import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import AccessToken

from models.models import GameRoom, Message, UserProfile, MatchHistory
from django.contrib.auth.models import User
from datetime import datetime

online_users = set()
random_match_users = set()
user_channel_names = {}
connected_users = {}

@database_sync_to_async
def get_user_info_from_token(jwt):
    token = AccessToken(jwt)
    user_id = token['user_id']
    user = User.objects.get(id=user_id)

    return user.profile


class NoticeConsumer(AsyncWebsocketConsumer):
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=message)

    async def connect(self):
        await self.accept()
        user = self.scope['user']
        connected_users[user.id] = self.channel_name
        user_channel_names[user.id] = user.username
        online_users.add(user)
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!',
            'userLine': len(online_users)
        }))

    async def disconnect(self, close_code):
        print('logout.......')
        online_users.discard(self.scope['user'])
        random_match_users.discard(self.scope['user'])
        user_id = self.scope['user'].id
        if user_id in connected_users:
            del connected_users[user_id]

        await self.channel_layer.group_discard(
            "online_users",
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            if data['message'] == 'ping':
                await self.send(text_data=json.dumps({'message': 'pong'}))

            if data['message'] == 'getRoomList':
                room_list = await self.get_room_list()

                await self.send(text_data=json.dumps({
                    'room_list': room_list
                }))

            if data['message'] == 'mypage':
                friend_list = await self.get_friend_on_line(data['friends'])

                await self.send(text_data=json.dumps(friend_list))

            if data['message'] == 'random_match':
                random_match_users.add(self.scope['user'])
                user_name = data['name']

                await self.send(text_data=json.dumps({
                    'message': user_name + 'is inserted!',
                    'len': len(random_match_users)
                }))

                if len(random_match_users) == 2:
                    try:
                        host = random_match_users.pop()
                        guest = random_match_users.pop()

                        random_match_room = await self.create_random_match_room(host, guest)
                        group_name = await self.generate_socket_room(random_match_room.id, host, guest)
                        message = await self.generate_users_information(host, guest)

                        await self.send_message_to_room("enter_room", group_name, message, random_match_room.id)
                    except Exception as e:
                        if random_match_room is not None:
                            await database_sync_to_async(random_match_room.delete)()
                        random_match_users.discard(host)
                        random_match_users.discard(guest)

            if data['message'] == 'random_match_cancel':
                random_match_users.discard(self.scope['user'])

                await self.send(text_data=json.dumps({
                    'message': 'match_canceled'
                }))
            if data['message'] == 'random_match_clear':
                room_id = data['room_id']
                await self.clear_random_match_room(room_id)

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'message': 'fail'}))

    @sync_to_async
    def clear_random_match_room(self, room_id):
        random_game_room = GameRoom.objects.filter(id=room_id)
        users = UserProfile.objects.filter(gmae_room=random_game_room)
        for user in users:
            user.game_room = None
            user.save()
        random_game_room.delete()
        random_game_room.save()

    @database_sync_to_async
    def exit_room(self, user):
        user_profile = user.profile
        user_profile.game_room = None
        user_profile.save()

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
            user = User.objects.get(username=name)
            status = user in online_users
            friends_status[name] = status

        return friends_status

    @database_sync_to_async
    def create_random_match_room(self, host, guest):
        game_room = GameRoom.objects.create(
            room_name="랜덤 매치 방",
            room_type=0,
            limits=2,
            password="",
            host=host.username
        )
        host.profile.game_room = game_room
        guest.profile.game_room = game_room
        host.profile.save()
        guest.profile.save()
        return game_room

    async def generate_socket_room(self, room_id, host, guest):
        group_name = f'random_match_{room_id}'
        host_channel_name = connected_users[host.id]
        guest_channel_name = connected_users[guest.id]
        await self.channel_layer.group_add(
            group_name,
            host_channel_name
        )
        await self.channel_layer.group_add(
            group_name,
            guest_channel_name
        )
        return group_name

    async def send_message_to_room(self, type_input, group_name, message, room_id):
        await self.channel_layer.group_send(
            group_name,
            {
                'type': type_input,
                'message': message,
                'room_id': room_id
            }
        )

    async def enter_room(self, event):
        message = event['message']
        room_id = event['room_id']
        await self.send(text_data=json.dumps({
            'type': 'enter_room',
            'message': message,
            'room_id': room_id
        }))

    def get_user_info(self, user):
        if user.profile.image:
            photo = user.profile.image.url
        else:
            photo = user.profile.picture
        return {
            'name': user.username, 'photo': photo
        }

    async def generate_users_information(self, host, guest):
        host_info = await sync_to_async(self.get_user_info)(host)
        guest_info = await sync_to_async(self.get_user_info)(guest)
        return [host_info, guest_info]

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))


class ChatConsumer(AsyncWebsocketConsumer):
    game_users = set()
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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
        data = json.loads(text_data)
        try:
            sender = data['sender']
            receiver = data['receiver']
            message = data['message']

            sender_profile = await self.get_user_profile(sender)
            receiver_profile = await self.get_user_profile(receiver)
            if message == '/invite':
                await self.send_invite_message('invited')

            elif message == 'start_game_in_chat':
                self.game_users.add(sender)
                if len(self.game_users) == 2:
                    service = NoticeConsumer
                    user = await self.get_user(sender_profile)
                    guest = await self.get_user(receiver_profile)
                    game_room = await service.create_random_match_room(user, guest)
                    await self.send_game_enter_message('enter_room', game_room.id)
                    self.game_users.clear()
            elif message == 'cancel_game_in_chat':
                await self.send_invite_message('match_cancel_chat')
                self.game_users.clear()
            else:
                await self.save_message(sender_profile, receiver_profile, message)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'sender': sender,
                        'message': message
                    }
                )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'message': 'fail'}))

    async def send_game_enter_message(self, message, room_id):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'start_game',
                'message': message,
                'room_id': room_id
            }
        )
    async def start_game(self, event):
        message = event['message']
        room_id = event['room_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'room_id': room_id
        }))
    async def send_invite_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_game',
                'message': message
            }
        )
    async def chat_game(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
    async def chat_message(self, event):
        sender = event['sender']
        message = event['message']

        # 클라이언트에게 메시지 전송
        await self.send(text_data=json.dumps({
            'sender': sender,
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, sender_profile, receiver_profile, message):
        message_instance = Message.objects.create(
            sender=sender_profile,
            receiver=receiver_profile,
            message=message
        )

    @database_sync_to_async
    def get_user_profile(self, id):
        return UserProfile.objects.get(oauth_id=id)
    @database_sync_to_async
    def get_user(self, profile):
        return User.objects.get(profile=profile)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        message = await self.generate_user_info_in_game_room(self.room_name)
        await self.send_connect_message('username', message)


    async def disconnect(self, close_code):
        """
        사용자와 WebSocket 연결이 끊겼을 때 호출
        """
        player = self.scope['user']

        # Leave room group
        type = await self.get_host(player)
        if type == 'host':
            await self.send_message("disconnect")
        else:
            message = await self.generate_user_info_in_game_room(self.room_name)
            await self.send_connect_message('username', message)


        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            if data['type'] == 'ready':
                user_number = data['user_num']
                await self.send_ready_message('ready', user_number)
            if data['type'] == 'start':
                await self.send_start_message('start')

            if data['type'] == 'user_update':
                if data['id'] == '1':
                    await self.channel_layer.group_send(
                        self.room_group_name, {'type': 'user_update', 'message': 'user_update', 'user': '1',
                                               'posY': data['posY'], 'skill': data['skill'],
                                               'skillpower': data["skillpower"], 'score': data['score']}
                    )
                elif data['id'] == '2':
                    await self.channel_layer.group_send(
                        self.room_group_name, {'type': 'user_update', 'message': 'user_update', 'user': '2',
                                               'posY': data['posY'], 'skill': data['skill'],
                                               'skillpower': data["skillpower"], 'score': data['score']}
                    )
            if data['type'] == 'ball_update':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {'type': 'ball_update', 'message': 'ball_update', 'posX': data['posX'], 'posY': data['posY']}
                )
            if data['type'] == 'win':
                player = self.scope['user']
                await set_win_lose(player, self.room_name)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'winner_message',
                        'message': 'exit',
                        'winner': await self.get_player_username(player),
                        'picture': await self.get_picture(player),
                    }
                )
                await self.send_message('end_game')
            if data['type'] == 'tournamentWin':
                await set_tournament_lose(self.scope['user'], self.room_name)
                await self.delete_done_room(self.room_name)
                await self.send_message('end_game')
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'message': 'fail'}))

    @database_sync_to_async
    def get_picture(self, user_profile):
        return user_profile.profile.get_picture()

    @database_sync_to_async
    def delete_done_room(self, id):
        game_room = GameRoom.objects.filter(id=id)
        game_room.delete()
    @database_sync_to_async
    def get_room_info(self, room_id):
        try:
            return GameRoom.objects.get(id=room_id)
        except GameRoom.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_user_profile_by_room_id(self, room):
        return UserProfile.objects.filter(game_room=room)
    
    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)
    @database_sync_to_async
    def get_player_username(self, player):
        return player.username
    
    @database_sync_to_async
    def get_user_participaints(self, room):
        return len(room.get_user())

    @database_sync_to_async
    def get_host(self, player):
        if GameRoom.objects.filter(id=self.room_name).exists():
            game = GameRoom.objects.get(id=int(self.room_name))
            if game.host == player.username:
                return 'host'
        return 'guest'

    @database_sync_to_async
    def generate_guest_profile(self, user_profiles, host_profile):
        guest_profiles = []
        for user_profile in user_profiles:
            if user_profile != host_profile:
                guest_info = {
                    'guest_name': user_profile.user.username,
                    'guest_picture': user_profile.get_picture()
                }
                guest_profiles.append(guest_info)
        return guest_profiles

    async def generate_user_info_in_game_room(self, room_id):
        room = await self.get_room_info(room_id)
        if room is not None:
            users_in_game_room = await self.get_user_profile_by_room_id(room)

            host_name = room.host
            participaints = await self.get_user_participaints(room)
            host = await self.get_user(host_name)
            host_picture = await self.get_picture(host)
            if participaints >= 2:
                guest_profiles = await self.generate_guest_profile(users_in_game_room, host.profile)
            else:
                guest_profiles = []
            
            return {
                'host_name': host_name,
                'host_picture': host_picture,
                'guests': guest_profiles
            }
    
    async def send_connect_message(self, type, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'fun_connect_message',
                'message': message,
                'input': type
            }
        )

    async def send_ready_message(self , message, user_number):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'fun_ready_message',
                'message' : message,
                'user_number' : user_number
            },
        )

    async def winner_message(self, event):
        message = event['message']
        winner = event['winner']
        picture = event['picture']
        await self.send(text_data=json.dumps({
            'type': message,
            'winner': winner,
            'picture': picture,
        }))
    
    async def send_start_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'fun_start_message',
                'message': message
            },
        )

    async def send_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'fun_send_message',
                'message': message
            },
        )

    async def fun_connect_message(self, event):
        message = event['message']
        type = event['input']
        await self.send(text_data=json.dumps({
            'type': type,
            'message': message
        }))

    async def fun_ready_message(self, event):
        message = event['message']
        user_number = event['user_number']
        await self.send(text_data=json.dumps({
            'type' : message,
            'user_number' : user_number
        }))

    async def fun_send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type' : message,
        }))

    async def fun_start_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': message
        }))

    async def user_update(self, event):
        message = event['message']
        user = event['user']
        posY = event['posY']
        skill = event['skill']
        score = event['score']
        skillpower = event['skillpower']
        await self.send(text_data=json.dumps({'type': message, 'user': user, 'posY': posY,
                                              'skill': skill, 'skillpower': skillpower, 'score': score}))

    async def ball_update(self, event):
        message = event['message']
        posX = event['posX']
        posY = event['posY']
        await self.send(text_data=json.dumps({'type': message, 'posY': posY, 'posX': posX}))

class TournamentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        message = await self.generate_user_info_in_game_room(self.room_name)
        await self.send_connect_message('username', message)
        

    async def disconnect(self, close_code):
        player = self.scope['user']
        type = await self.get_host(player)
        if type == 'host':
            await self.send_message("disconnect")
        else:
            message = await self.generate_user_info_in_game_room(self.room_name)
            await self.send_connect_message('username', message)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        try:
            if data['type'] == 'ready':
                user_number = data['user_num']
                await self.send_ready_message('ready', user_number)
            if data['type'] == 'start':
                room1 = await self.create_game_room(data['host1'])
                room2 = await self.create_game_room(data['host2'])
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'tournamnet_start',
                        'room1': room1,
                        'room2': room2
                    }
                )
            if data['type'] == 'finalReady':
                user_number = data['user_num']
                await self.send_ready_message('finalReady', user_number)

            if data['type'] == 'winner':
                player = self.scope['user']
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'winner_message',
                        'message': 'win',
                        'winner': await self.get_player_nickname(player),
                        'picture': await self.get_picture(player.profile),
                        'roomId': data['roomId'],
                    }
                )
            if data['type'] == 'isPresent':
                exist = await self.is_present_room(data['roomId1'], data['roomId2'])
                if exist is True:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'start_message',
                            'message': 'remove'
                        }
                    )
            if data['type'] == 'finalStart':
                nick_name = await self.get_player_nickname(self.scope['user'])
                roomID = await self.create_game_room(nick_name)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'tournamnet_final_start',
                        'roomId': roomID
                    }
                )
            if data['type'] == 'finalWinner':
                player = self.scope['user']

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'winner_message',
                        'message': 'finalWinner',
                        'winner': await self.get_player_nickname(player),
                        'picture': await self.get_picture(player.profile),
                        'roomId': self.room_name,
                    }
                )
                await self.delete_room(int(self.room_name))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'message': 'fail'}))

    async def start_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'type': message}))

    async def tournamnet_start(self, event):
        room1 = event['room1']
        room2 = event['room2']
        await self.send(text_data=json.dumps({
            'type': 'start',
            'room1': room1,
            'room2': room2,
        }))

    async def tournamnet_final_start(self, event):
        roomId = event['roomId']
        await self.send(text_data=json.dumps({
            'type': 'finalStart',
            'roomId': roomId,
        }))

    async def fun_start_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': message
        }))

    async def winner_message(self, event):
        message = event['message']
        winner = event['winner']
        picture = event['picture']
        roomId = event['roomId']
        await self.send(text_data=json.dumps({
            'type': message,
            'nickname': winner,
            'picture': picture,
            'roomId': roomId,
        }))

    @database_sync_to_async
    def is_present_room(self, id1, id2):
        return not GameRoom.objects.filter(id=id1).exists() and not GameRoom.objects.filter(id=id2).exists()

    @database_sync_to_async
    def get_room_info(self, room_id):
        try:
            return GameRoom.objects.get(id=room_id)
        except GameRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user_profile_by_room_id(self, room):
        return UserProfile.objects.filter(game_room=room)

    @database_sync_to_async
    def get_user_profile(self, username):
        return User.objects.get(username=username).profile

    @database_sync_to_async
    def get_picture(self, user_profile):
        return user_profile.get_picture()

    @database_sync_to_async
    def get_user_participaints(self, room):
        return len(room.get_user())

    @database_sync_to_async
    def get_player_nickname(self, player):
        return player.profile.nick_name

    @database_sync_to_async
    def generate_guest_profile(self, user_profiles, host_profile):
        guest_profiles = []
        for user_profile in user_profiles:
            if user_profile != host_profile:
                guest_info = {
                    'guest_name': user_profile.nick_name,
                    'guest_picture': user_profile.get_picture()
                }
                guest_profiles.append(guest_info)
        return guest_profiles

    async def generate_user_info_in_game_room(self, room_id):
        room = await self.get_room_info(room_id)
        if room is not None:
            users_in_game_room = await self.get_user_profile_by_room_id(room)

            host_name = room.host
            participaints = await self.get_user_participaints(room)
            host = await self.get_user_profile(host_name)
            host_picture = await self.get_picture(host)

            if participaints >= 2:
                guest_profiles = await self.generate_guest_profile(users_in_game_room, host)
            else:
                guest_profiles = []

            return {
                'host_name': host.nick_name,
                'host_picture': host_picture,
                'guests': guest_profiles
            }

    @database_sync_to_async
    def create_game_room(self, host_name):
        host = UserProfile.objects.get(nick_name=host_name)
        game_room = GameRoom.objects.create(
            room_name='Tournament' + host.nick_name,
            room_type=0,
            limits=2,
            password="",
            host=host.user.username
        )
        host.game_room = game_room
        host.save()
        return game_room.id

    @database_sync_to_async
    def delete_room(self, id):
        game = GameRoom.objects.filter(id=id)
        game.delete()

    @database_sync_to_async
    def get_host(self, player):
        if GameRoom.objects.filter(id=self.room_name).exists():
            game = GameRoom.objects.get(id=int(self.room_name))
            if game.host == player.username:
                return 'host'
        return 'guest'

    async def send_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'fun_send_message',
                'message': message
            },
        )

    async def send_connect_message(self, type, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'fun_connect_message',
                'message': message,
                'input': type
            }
        )

    async def send_ready_message(self, message, user_number):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'fun_ready_message',
                'message': message,
                'user_number': user_number
            },
        )

    async def send_start_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'fun_start_message',
                'message': message
            },
        )

    async def fun_connect_message(self, event):
        message = event['message']
        type = event['input']
        await self.send(text_data=json.dumps({
            'type': type,
            'message': message
        }))

    async def fun_ready_message(self, event):
        message = event['message']
        user_number = event['user_number']
        await self.send(text_data=json.dumps({
            'type': message,
            'user_number': user_number
        }))

    async def fun_send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': message,
        }))


@database_sync_to_async
def set_win_lose(winner, room_id):
    users = UserProfile.objects.filter(game_room_id=room_id)
    loser = users.exclude(id=winner.id).first()

    winner.profile.total_win += 1
    loser.total_lose += 1
    winner.profile.save()
    loser.save()

    MatchHistory.objects.create(
        opponent_name=loser.user.username,
        user=winner.profile,
        result='win',
        game_type='0',
        match_date=datetime.now()
    )
    MatchHistory.objects.create(
        opponent_name=winner.username,
        user=loser,
        result='lose',
        game_type='0',
        match_date=datetime.now()
    )


@database_sync_to_async
def set_tournament_lose(winner, room_id):
    users = UserProfile.objects.filter(game_room_id=room_id)
    loser = users.exclude(id=winner.id).first()

    loser.total_lose += 1
    loser.save()

    MatchHistory.objects.create(
        opponent_name='tournament',
        user=loser,
        result='lose',
        game_type='1',
        match_date=datetime.now()
    )


@database_sync_to_async
def set_tournament_win(winner, room_id):
    user = winner.profile

    user.total_win += 1
    user.save()
    MatchHistory.objects.create(
        opponent_name='tournament',
        user=user,
        result='win',
        game_type='1',
        match_date=datetime.now()
    )