from django.contrib.auth.hashers import check_password

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async

from .models.player import Player
from .models.room import Room

import json
from collections import defaultdict


class GameRoomConsumer(AsyncWebsocketConsumer):
    room_connection_counts = defaultdict(lambda: 0)
    room_password_cache = {}

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f'game_{self.room_id}'
        provided_password = self.scope['url_route']['kwargs'].get('room_password')

        connection_accepted = False

        try:
            self.room_connection_counts[self.room_id] += 1

            if self.room_id in self.room_password_cache:
                # Check password
                if not check_password(provided_password, self.room_password_cache[self.room_id]):
                    raise DenyConnection()
            else:
                # Add expected password to cache
                room = await database_sync_to_async(Room.objects.get)(id=self.room_id)
                self.room_password_cache[self.room_id] = room.password
                # Check password
                if not check_password(provided_password, self.room_password_cache[self.room_id]):
                    raise DenyConnection()

            self.player_name = self.scope['url_route']['kwargs']['username']

            # Add player to DB
            self.player, _ = await database_sync_to_async(
                Player.objects.get_or_create
            )(room_id=self.room_id, name=self.player_name)

            # Join room group
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

            await self.accept()
            connection_accepted = True
            print("Connection Count:", self.room_connection_counts[self.room_id])

        finally:
            # Decrement connection count if accept() was not called
            if not connection_accepted:
                self.room_connection_counts[self.room_id] -= 1

    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
        try:
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
        except AttributeError:
            pass


        self.room_connection_counts[self.room_id] -= 1
        print("Connection Count:", self.room_connection_counts[self.room_id])
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

    async def send_error_response(self, error_message):
        error_data = {
            'type': 'error',
            'message': error_message
        }
        await self.send(text_data=json.dumps(error_data))
        await self.close()
    # Message Definitions
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
