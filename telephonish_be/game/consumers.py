from django.contrib.auth.hashers import check_password
from django.db.models import F

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models.player import Player
from .models.room import Room

import json
from collections import defaultdict
import logging
import secrets

logger = logging.getLogger(__name__)


class GameRoomConsumer(AsyncWebsocketConsumer):
    room_connection_counts = defaultdict(lambda: 0)
    room_players_ready_to_start = defaultdict(set)
    room_players_done_story = defaultdict(set)
    room_players_done_drawing = defaultdict(set)

    room_password_not_required = set()
    room_password_cache = {}
    player_tokens = {}

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f'game_{self.room_id}'
        self.player_name = self.scope['url_route']['kwargs']['player_name']
        provided_password = self.scope['url_route']['kwargs'].get('room_password')

        self.room_connection_counts[self.room_id] += 1
        logger.info("Connection Count: %d", self.room_connection_counts[self.room_id])

        try:
            logger.info("authenticating room password")
            authenticated = await self.authenticate_room_password(provided_password)

            if authenticated:
                # Add player to DB
                logger.info("adding player")
                self.player = await database_sync_to_async(
                    Player.objects.create
                )(room_id=self.room_id, name=self.player_name)

                # Generate and store token
                logger.info("generating token")
                self.player_token = await self.generate_player_token()

                # Join room group
                logger.info("joining room")
                await self.channel_layer.group_add(
                    self.room_group_id,
                    self.channel_name
                )

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_id,
                    {
                        'type': 'player_connect',
                        'message': f'{self.player_name} has joined the game room.'
                    }
                )

                logger.info("accepting connection")
                await self.accept()

                logger.info("sending token to client")
                await self.send_player_token()

        except Exception as err:
            logger.error(err)

    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )

        if hasattr(self, "player"):
            # Delete player from DB
            await database_sync_to_async(self.player.delete)()

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_id,
                {
                    'type': 'player_disconnect',
                    'message': f'{self.player_name} has left the game room.'
                }
            )

            # Remove auth token
            try:
                # Delete player token
                del self.player_tokens[self.player_token]
            except KeyError:
                pass

            # Clear room-related data
            self.room_players_ready_to_start[self.room_id].discard(self.player_name)
            self.room_players_done_story[self.room_id].discard(self.player_name)
            self.room_players_done_drawing[self.room_id].discard(self.player_name)

        # Decrement room connection count
        self.room_connection_counts[self.room_id] = max(
            self.room_connection_counts[self.room_id] - 1,
            0
        )
        logger.info("Connection Count: %d", self.room_connection_counts[self.room_id])

        # Clean up room if no connections remain
        if self.room_connection_counts[self.room_id] == 0:
            await self.clean_up_room()

        await self.close()

    async def authenticate_room_password(self, provided_password):
        if self.room_id in self.room_password_not_required:
            return True

        if self.room_id in self.room_password_cache:
            # Check password
            if not check_password(provided_password, self.room_password_cache[self.room_id]):
                await self.accept_and_close_with_message("invalid_room_password")
                return False

        else:
            # Retrieve room from the database
            room = await database_sync_to_async(Room.objects.get)(id=self.room_id)

            if room.password_required:
                # Check password
                if not check_password(provided_password, room.password):
                    await self.accept_and_close_with_message("invalid_room_password")
                    return False

                # Add valid password to cache
                self.room_password_cache[self.room_id] = room.password

            else:
                # Password not required for this room
                self.room_password_not_required.add(room.id)
                return True

        return True

    async def generate_player_token(self):
        token = secrets.token_hex(16)
        self.player_tokens[token] = {
            'name': self.player_name,
            'room_id': self.room_id
        }
        return token

    async def send_player_token(self):
        token_data = {
            'type': 'player_token',
            'token': self.player_token,
            'player_id': self.player.id
        }
        await self.send(text_data=json.dumps(token_data))

    async def authenticate_player_token(self, provided_token):
        player_info = self.player_tokens.get(provided_token)
        if (
            player_info
            and player_info["name"] == self.player_name
            and player_info["room_id"] == self.room_id
        ):
            return True
        self.accept_and_close_with_message("invalid_player_token")
        return False

    async def accept_and_close_with_message(self, message):
        await self.accept()
        bad_authentication_data = {
            'type': 'connection_closed',
            'message': message,
        }
        await self.send(text_data=json.dumps(bad_authentication_data))
        await self.close()

    async def clean_up_room(self):
        # Perform any necessary cleanup operations for the room
        room_id = self.room_id

        # Delete the room from the database
        # await database_sync_to_async(Room.objects.filter(id=room_id).delete)()

        # Clear any cached room password
        if room_id in self.room_password_cache:
            del self.room_password_cache[room_id]

        # Clear room-related data
        del self.room_players_ready_to_start[room_id]
        del self.room_players_done_story[room_id]
        del self.room_players_done_drawing[room_id]

        # Optionally, perform additional cleanup tasks specific to your application

        logger.info("Room %s has been cleaned up.", room_id)

    # Receiver Logic
    async def receive(self, text_data):
        logger.info(text_data)

        text_data_json = json.loads(text_data)
        provided_token = text_data_json['player_token']
        authenticated = self.authenticate_player_token(provided_token)

        if authenticated:
            message_type = text_data_json['type']
            message = text_data_json['message']

            should_send = False
            if message_type == "ready_to_start":
                self.room_players_ready_to_start[self.room_id].add(self.player_name)
                if (
                        len(self.room_players_ready_to_start[self.room_id]) > 1
                        and len(self.room_players_ready_to_start[self.room_id]) == self.room_connection_counts[self.room_id]
                ):
                    await self.increment_room_round_number(self.room_id)
                    should_send = True
            elif message_type == "done_writing_story":
                self.room_players_done_story[self.room_id].add(self.player_name)
                if len(self.room_players_done_story[self.room_id]) == self.room_connection_counts[self.room_id]:
                    await self.increment_room_round_number(self.room_id)
                    should_send = True
            elif message_type == "done_drawing":
                self.room_players_done_drawing[self.room_id].add(self.player_name)
                if len(self.room_players_done_drawing[self.room_id]) == self.room_connection_counts[self.room_id]:
                    await self.increment_room_round_number(self.room_id)
                    should_send = True

            if should_send:
                await self.channel_layer.group_send(
                    self.room_group_id,
                    {
                        'type': message_type,
                        'player_name': self.player_name,
                        'message': message,
                    }
                )

    # Message Definitions
    async def ready_to_start(self, event):
        logger.info(event)

        player_name = event['player_name']
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'ready_to_start',
            'player_name': player_name,
            'message': message
        }))

    async def done_writing_story(self, event):
        logger.info(event)

        player_name = event['player_name']
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'done_writing_story',
            'player_name': player_name,
            'message': message
        }))

    async def done_drawing(self, event):
        logger.info(event)

        player_name = event['player_name']
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'done_drawing',
            'player_name': player_name,
            'message': message
        }))

    async def player_connect(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'player_connect',
            'message': message
        }))

    async def player_disconnect(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'player_disconnect',
            'message': message
        }))

    # utils
    async def increment_room_round_number(self, room_id):
        await database_sync_to_async(Room.objects.filter(id=room_id).update)(
            current_round_number=F('current_round_number') + 1)



