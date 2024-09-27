from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, code):
        #leave room
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    #receive massage from ws
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        
        conversation_id = data['data']['conversation_id']
        sent_to_id = data['data']['sent_to_id']
        name = data['data']['name']
        body = data['data']['body']
        
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'body': body,
                'name': name,
            }
        )
        
        await self.save_message(conversation_id, body, sent_to_id)
        
    #send message
    async def chat_message(self, event):
        name = event['name']
        body = event['body']
        
        await self.send(text_data=json.dumps({
            'body': body,
            'name': name,
        }))
        
    @sync_to_async
    def save_message(self, conversation_id, body, sent_to_id):
        print('scope', self.scope)
        
        user = self.scope['user']  # Récupérer l'utilisateur connecté
                
        Message.objects.create(
            conversation_id=conversation_id, 
            body=body, 
            sent_to_id=sent_to_id, 
            author=user or ''
        )
