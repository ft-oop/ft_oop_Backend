import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
import sys
from .models.models import UserProfile, GameRoom
from django.contrib.auth.models import User
online_users = set()


# Unused class
# class GameConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         global online_users
#         online_users.add(self.user.id)
#         message = {"type": "user_status", "user_id": self.user.id, "status": "online"}
#         await self.send_to_mypage(message)
#         # await self.connect_default()

#         await self.accept()

#     '''
#     async def connect_default(self):
#         self.group_name = 'default'

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#     '''

#     async def connect_room_id(self, room_id):
#         await self.disconnect_room()
#         self.group_name = f'game/{room_id}'
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#     async def connect_room_list(self):
#         await self.disconnect_room()
#         self.group_name = f'room_list'
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#     async def connect_mypage(self):
#         await self.disconnect_room()
#         self.group_name = f'mypage'
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         global online_users
#         await self.send(text_data=json.dumps({
#             'message': online_users
#         }))

#     async def disconnect_room(self):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def disconnect(self, close_code):
#         global online_users
#         online_users.remove(self.user.id)
#         message = {"type": "user_status", "user_id": self.user.id, "status": "offline"}
#         await self.send_to_mypage(message)

#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'broadcast_message',
#                 'message': message
#             }
#         )

#     async def send_to_mypage(self, message):
#         await self.channel_layer.group_send(
#             'mypage',
#             {
#                 'type': 'broadcast_message',
#                 'message': message
#             }
#         )

#     async def send_to_room_list(self, message):
#         await self.channel_layer.group_send(
#             'room_list',
#             {
#                 'type': 'broadcast_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def broadcast_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))


# class OopConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         global online_users
#         online_users.add(self.user.id)
#         message = {"type": "user_status", "user_id": self.user.id, "status": "online"}
#         await self.channel_layer.group_add(
#             "online_users",
#             self.channel_name
#         )
#         await self.send(message)
#         await self.accept()

#     async def disconnect(self, close_code):
#         global online_users
#         online_users.remove(self.user.id)
#         message = {"type": "user_status", "user_id": self.user.id, "status": "offline"}
#         await self.send(message)

#         # Leave room group
#         await self.channel_layer.group_discard(
#             "online_users",
#             self.channel_name
#         )

#     # 클라이언트에서 서버로 메세지를 보낼 때 사용
#     # 클라이언트로부터 메세지를 받았을 때 호출되는 함수
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             "online_users",
#             {
#                 'type': 'broadcast_message',
#                 'message': message
#             }
#         )

#     # 서버가 특정 그룹의 클라이언트에게 메세지를 보낼 때 사용하는 함수
#     async def broadcast_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
@database_sync_to_async
def get_user_info_from_token(jwt):
    token = AccessToken(jwt)
    user_id = token['user_id']
    user = UserProfile.objects.get(id=user_id)

    return user

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user = self.scope['user']
        online_users.add(self.scope['user']) 
        print(len(online_users))
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!',
            'userLine' : len(online_users)
        }))

    async def disconnect(self, close_code):
        print("logout.......")
        online_users.remove(self.scope['user'])
    
    async def receive(self, text_data):
        print("received message: " + text_data)
        try:
            data = json.loads(text_data)
            
            if data['message'] == 'ping':
                print(data['message'])
                await self.send(text_data=json.dumps({'message': 'pong'}))

            if data['message'] == 'getRoomList':
                room_list = await self.get_room_list()

                await self.send(text_data=json.dumps({
                    'room_list' : room_list
                }))
            
            if data['message'] == 'mypage':
                friend_list = await self.get_friend_on_line(data['friends'])

                await self.send(text_data=json.dumps(friend_list))
            
            if data['message'] == 'chat':
                user = self.scope['user']
                receiver = data['receiver']
                message = data['content']

                user_profile = get_object_or_404(User, username=user).profile
                receiver_profile = get_object_or_404(User, username=receiver).profile

                message_instance = Message.objects.create(
                    sender=user_profile,
                    receiver=receiver_profile,
                    message=message
                )
                await self.send(text_data=json.dumps({
                    'sender': user,
                    'receiver': receiver,
                    'content': message
                }))
                
            # if data['message'] == 'login':
            #     jwt = data['token']
            #     user = await get_user_info_from_token(jwt)
            #     online_users.add(user)
            #     print(len(online_users))
            #     await self.send(text_data=json.dumps({
            #         'message': 'user login successful!',
            #         'userLen' : len(online_users)
            #     }))
            # if data['message'] == 'logout':
            #     jwt = data['token']
            #     user = await get_user_info_from_token(jwt)
            #     online_users.remove(user)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'message': 'fail'}))

    @sync_to_async
    def get_room_list(self):
        return [{
        'id': room.get_room_id(),
        'name': room.get_room_name(),
        'type': room.get_room_type(),
        'limits': room.get_limits(),
        'password': room.get_pass_word(),
        'host': room.get_host(),
        'users': room.get_user(),
        'participant': room.get_room_person()
    } for room in GameRoom.objects.all()]
    
    @sync_to_async
    def get_friend_on_line(self, friends):
        friends_status = {}
        for friend in friends:
            name = friend.get('user_name')
            user = User.objects.get(username=name).profile
            status = user in online_users
            friends_status[name] = status
        
        return friends_status