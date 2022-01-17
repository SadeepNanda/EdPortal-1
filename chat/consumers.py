import json 
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        user = self.scope['user']
        chat_room = f'user_chatroom_{user.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_recieve(self, event):
        print("recieved", event)
        recieved_data = json.loads(event['text'])
        msg = recieved_data.get('message')
        sent_by_id = recieved_data.get('sent_by')
        send_to_id = recieved_data.get('send_to')

        if not msg:
            print("Error:: no message")
            return False
        
        sent_by_user = await self.get_user_objects(sent_by_id)
        send_to_user = await self.get_user_objects(send_to_id)

        if not sent_by_user:
            print("Error:: sent by user is incorrect")
        if not send_to_user:
            print("Error:: send to user is incorrect")

        other_user_chat_room = f'user_chatroom_{send_to_id}'

        self.user = self.scope['user']

        response = {
            'message' : msg,
            'sent_by' : self.user.id
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text' : json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text' : json.dumps(response)
            }
        )

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def chat_message(self, event):
        print("chat message", event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_objects(self, user_id):
        qs = User.objects.filter(id = user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        
        return obj