from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = f'game_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_connect',
                'message': f'{self.username} has joined the game room.'
            }
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'player_disconnect',
                'message': f'{self.username} has left the game room.'
            }
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'username': self.username,
                'message': message
            }
        )

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
