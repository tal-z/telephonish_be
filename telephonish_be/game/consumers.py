from django.contrib.auth.hashers import check_password

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
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
    room_password_cache = {}
    player_tokens = {}

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f'game_{self.room_id}'
        self.player_name = self.scope['url_route']['kwargs']['username']
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

        self.room_connection_counts[self.room_id] = max(
            self.room_connection_counts[self.room_id] - 1,
            0
        )
        logger.info("Connection Count: %d", self.room_connection_counts[self.room_id])
        # TODO: Clean up room if no connections remain

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'game_message',
                'username': self.username,
                'message': message
            }
        )

    async def authenticate_room_password(self, provided_password):
        if self.room_id in self.room_password_cache:
            # Check password
            if not check_password(provided_password, self.room_password_cache[self.room_id]):
                await self.accept_and_close_with_message("invalid_room_password")
                return False

        else:
            # Add expected password to cache
            room = await database_sync_to_async(Room.objects.get)(id=self.room_id)
            self.room_password_cache[self.room_id] = room.password
            # Check password
            if not check_password(provided_password, self.room_password_cache[self.room_id]):
                await self.accept_and_close_with_message("invalid_room_password")
                return False
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
            'token': self.player_token
        }
        await self.send(text_data=json.dumps(token_data))

    # Message Definitions

    async def accept_and_close_with_message(self, message):
        await self.accept()
        bad_authentication_data = {
            'type': 'connection_closed',
            'message': message,
        }
        await self.send(text_data=json.dumps(bad_authentication_data))
        await self.close()

    async def game_message(self, event):
        username = event['username']
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'game_message',
            'username': username,
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
