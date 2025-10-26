from channels.generic.websocket import AsyncWebsocketConsumer
import json


class BattleConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time battle functionality.
    This is a placeholder for future multiplayer features.
    """
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'battle_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'battle_message',
                'message': text_data_json
            }
        )
    
    async def battle_message(self, event):
        message = event['message']
        
        await self.send(text_data=json.dumps(message))
