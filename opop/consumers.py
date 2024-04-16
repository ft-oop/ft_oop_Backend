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

        # Send message to WebSocket
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
        # if self.user.username in user_channel_names:
        #     del user_channel_names[self.user.username]
        online_users.remove(self.scope['user'])
        user_id = self.scope['user'].id
        if user_id in connected_users:
            del connected_users[user_id]

        await self.channel_layer.group_discard(
            "online_users",
            self.channel_name
        )

    async def receive(self, text_data):
        print('received message: ' + text_data)
        try:
            data = json.loads(text_data)
            print('type is..... ' + data['message'])

            if data['message'] == 'ping':
                print(data['message'])
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
                # async with self.lock:
                user = self.scope['user']
                random_match_users.add(user)
                user_name = data['name']
                print(user_name)
                # 성공적으로 큐에 담겼다면, 메세지를 보냅니다.
                await self.send(text_data=json.dumps({
                    'message': user_name + 'is inserted!',
                    'len': len(random_match_users)
                }))
                # 2명의 유저가 매칭 큐에 담겼다면, 방을 생성합니다.
                # 이후 해당 유저들을 같은 소켓 룸에 담아두고, 메세지를 전송합니다.
                if len(random_match_users) == 2:
                    try:
                        host = random_match_users.pop()
                        guest = random_match_users.pop()

                        random_match_room = await self.create_random_match_room(host)
                        group_name = await self.generate_socket_room(random_match_room.id, host, guest)
                        print('generate_socket_room clear!!!!!')
                        message = await self.generate_users_information(host, guest)
                        print('create_message_clear!')


                        await self.send_message_to_room("enter_room", group_name, message)
                    except Exception as e:
                        print('에러 발생!', e)
                        if random_match_room is not None:
                            await database_sync_to_async(random_match_room.delete)()
                        random_match_users.remove(host)
                        random_match_users.remove(guest)

            if data['message'] == 'random_match_cancel':
                user_profile = self.scope['user']

                random_match_users.remove(user_profile)

                await self.send(text_data=json.dumps({
                    'message': 'match canceled!'
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
    def create_random_match_room(self, host):
        return GameRoom.objects.create(
            room_name="랜덤 매치 방",
            room_type=0,
            limits=2,
            password="",
            host=host.username
        )

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

    async def send_message_to_room(self, type_input, group_name, message):
        print('메세지 전송을 시작합니다...')
        await self.channel_layer.group_send(
            group_name,
            {
                'type': type_input,
                'message': message
            }
        )

    async def enter_room(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'enter_room',
            'message': message
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
        try:
            data = json.loads(text_data)
            sender = data['sender']
            receiver = data['receiver']
            message = data['message']

            sender_profile = await self.get_user_profile(sender)
            receiver_profile = await self.get_user_profile(receiver)
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

    async def chat_message(self, event):
        sender = event['sender']
        message = event['message']

        print(sender)
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

class GameConsumer(AsyncWebsocketConsumer):
    user = []
    game = False

    host = ''

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'
        player = self.scope['user']
        if len(self.user) > 2:
            await self.send(text_data=json.dumps({'message': 'full room'}))
        
        self.user.append([player, False])
        print(self.user)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        if len(self.user) == 1:
            await self.accept()
            await self.send(text_data=json.dumps({"type": "user", "user": "1"}))
            await self.channel_layer.group_send(
                self.room_group_name, {'type': 'start_message', 'message': "user1 connect"},
            )
            self.host = self.user[0][0].username

        elif len(self.user) == 2:
            await self.accept()
            await self.send(text_data=json.dumps({"type": "user", "user": "2"}))
            await self.channel_layer.group_send(
                self.room_group_name, {'type': 'start_message', 'message': "user2 connect"},
            )

    
    async def disconnect(self, close_code):
        """
        사용자와 WebSocket 연결이 끊겼을 때 호출
        """
        player = self.scope['user']
        for p in self.user:
            if p[0] == player:
                self.user.remove(p)

        # Leave room group
        type = await self.get_host(player)
        if type == 'host':
            await self.channel_layer.group_send(
                self.room_group_name, {'type': 'start_message', 'message': "disconnect"},
            )
            
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        try:
            if data['type'] == 'ready':
                if data['user'] == "1":
                    self.user[0][1] = True
                elif data['user'] == "2":
                    self.user[1][1] = True
            if self.user[0][1] and self.user[1][1]:
                self.game = True
                self.user[0][1] = False
                self.user[1][1] = False
                await self.channel_layer.group_send(
                    self.room_group_name, {'type': 'start_message', 'message' : 'start'}
                )
                
            if data['type'] == 'user_update':
                if data['id'] == '1':
                    await self.channel_layer.group_send(
                        self.room_group_name, {'type': 'user_update', 'message' : 'user_update', 'user' : '1',
                                               'posY' : data['posY'], 'skill' : data['skill'], 'skillpower' : data["skillpower"], 'score' : data['score']}
                    )
                elif data['id'] == '2':
                    await self.channel_layer.group_send(
                        self.room_group_name, {'type': 'user_update', 'message' : 'user_update', 'user' : '2',
                                               'posY' : data['posY'], 'skill' : data['skill'], 'skillpower' : data["skillpower"], 'score' : data['score']}
                    )
            if data['type'] == 'ball_update':
                await self.channel_layer.group_send(
                        self.room_group_name, {'type': 'ball_update', 'message' : 'ball_update', 'posX' : data['posX'], 'posY' : data['posY']}
                    )
            if data['type'] == 'win':
                winner = self.scope['user']
                for p in self.user:
                    if p[0] != winner:
                        loser = p[0]
                        break
                await self.set_win_lose(winner, loser)
                await self.channel_layer.group_send(
                    self.room_group_name, {'type': 'start_message', 'message' : 'end_game'}
                )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'message': 'fail'}))

    async def start_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'type': message}))

    async def user_update(self, event):
        message = event['message']
        user = event['user']
        posY = event['posY']
        skill = event['skill']
        score = event['score']
        skillpower = event['skillpower']
        await self.send(text_data=json.dumps({'type': message, 'user' : user, 'posY' : posY,
                                              'skill' : skill, 'skillpower' : skillpower, 'score' : score}))
    async def ball_update(self, event):
        message = event['message']
        posX = event['posX']
        posY = event['posY']
        await self.send(text_data=json.dumps({'type': message, 'posY' : posY, 'posX' : posX}))
    
    async def picture_update(self, event):
        message = event['message']
        user_info = []
        for u in self.user:
            user_profile = u[0].profile
            user_info.append({
                'username': u.username,
                'picture': user_profile.get_picture()
            })
        await self.send(text_data=json.dumps({'type': user_info}))

    @database_sync_to_async
    def get_host(self, player):
        if self.host == player.username:
            return 'host'
        return 'guest'

    @database_sync_to_async
    def set_win_lose(self, winner, loser):
        winner.profile.total_win += 1
        loser.profile.total_lose += 1
        MatchHistory.objects.create(
            opponent_name=loser.username,
            user = winner.profile,
            result = 'win',
            game_type = 0,
            match_date = datetime.now()
        )
        MatchHistory.objects.create(
            opponent_name=winner.username,
            user = loser.profile,
            result = 'lose',
            game_type = 0,
            match_date = datetime.now()
        )