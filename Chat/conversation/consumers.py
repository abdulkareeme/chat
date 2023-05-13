from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message , Conversation
from core.models import User
import json

class ChatConsumer(AsyncWebsocketConsumer):
    # conversation = None
    # receiver=None
    # sender = None
    async def connect(self):
        # Join a room for the two users' private chat
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'private_chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # sender = self.scope['user']
        await self.get_data()
        # Send the messages to the user
        # other_user = User.objects.get(username=self.scope['url_route']['kwargs']['other_user'])
        # messages = await self.get_latest_messages(self.sender, self.receiver)
        # for message in messages:
        #     await self.send(text_data=json.dumps({
        #         'message': message.content,
        #         'sender': message.sender.username,
        #         'receiver': message.receiver.username,
        #         'time': message.time
        #     }))

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the private chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive a message from one of the users and send it to the other user in the room
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # sender = self.scope['user']
        #TODO make it async
        # self.receiver = User.objects.get(username=text_data_json['receiver'])       
        # Save the new message to the database
        message = await self.create_message(self.sender, self.receiver, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'sender': message.sender.username,
                'receiver': message.receiver.username,
                'time' : message.time
            }
        )

    async def chat_message(self, event):
        # Receive a message from the channel layer, and send it to the user who is not the sender
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        time = event['time']

        if self.scope['user'].username == receiver:
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender,
                'receiver': receiver,
                'time': time
            }))
    @database_sync_to_async
    def create_message(self, sender, receiver, message):
        # Create a new message object and save it to the database
        return Message.objects.create(sender=sender, receiver=receiver, content=message,conversation=self.conversation)
    
    @database_sync_to_async
    def get_data(self ,sender=None):
        self.sender = User.objects.get(username='abdulkareem')
        self.receiver = User.objects.get(username=self.scope['url_route']['kwargs']['other_user'])
        self.conversation = Conversation.objects.filter(user1=self.sender, user2=self.receiver).union(
            Conversation.objects.filter(user1=self.receiver, user2=self.sender))[0]
    # @database_sync_to_async
    # def get_latest_messages(self, sender, receiver):
    #     # Return the ten most recent messages between the two users
    #     return Message.objects.filter(conversation = self.conversation)[0:10]
        