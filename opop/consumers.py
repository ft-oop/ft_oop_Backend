import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
import sys
from .models.models import UserProfile, GameRoom, Message
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
online_users = set()
random_match_users = set()


@database_sync_to_async
def get_user_info_from_token(jwt):
    token = AccessToken(jwt)
    user_id = token['user_id']
    user = User.objects.get(id=user_id)

    return user.profile

class ChatConsumer(AsyncWebsocketConsumer):

    async def create_room_and_enter_users(self):
        users = list(random_match_users)
        user1, user2 = users[0], users[1]
        room = await self.create_random_match_room(user1)

        target_users = [
        {'name': user1.user.username, 'photo': user1.picture},
        {'name': user2.user.username, 'photo': user2.picture}
    ]

        await self.send(text_data=json.dumps({
                'type': 'enter_room',
                'room_id': room.id,
                # 'host': user1.user.username,
                'target': target_users
            }))
        
        random_match_users.clear()

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
        if (len(random_match_users) == 2):
            await self.create_room_and_enter_users()
            # self.enter_room
        try:
            data = json.loads(text_data)
            print('type is..... ' + data['message'])
            
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
                print("message is chat..!!" + data['receiver'])
                
                sender = data['sender']
                receiver = data['receiver']
                message = data['input']

                sender_profile = await self.get_user_profile(sender)
                receiver_profile = await self.get_user_profile(receiver)
                await self.save_message(sender_profile, receiver_profile, message)
               
                await self.send(text_data=json.dumps({
                    'sender': sender,
                    'receiver': receiver,
                    'input': message
                }))
            
            if data['message'] == 'random_match':
                user_profile = self.scope['user']
                random_match_users.add(user_profile)
                user_name = data['name']
                if (len(random_match_users) == 2):
                    await self.create_room_and_enter_users()
                else:
                    await self.send(text_data=json.dumps({
                        'message': user_name + 'is inserted!'
                    }))

            if data['message'] == 'random_match_cancel':
                user_profile = self.scope['user']

                random_match_users.remove(user_profile)

                await self.send(text_data=json.dumps({
                    'message': 'match canceled!'
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
    
    @database_sync_to_async
    def get_user_profile(self, username):
        return User.objects.get(username=username).profile

    @database_sync_to_async
    def save_message(self, sender_profile, receiver_profile, message):
         message_instance = Message.objects.create(
                    sender=sender_profile,
                    receiver=receiver_profile,
                    message=message
                )
    
    @database_sync_to_async
    def create_random_match_room(self, user1):
        return GameRoom.objects.create(
                    room_name="랜덤 매치 방",
                    room_type=0,
                    limits=2,
                    password="",
                    host=user1.user.username
                )
