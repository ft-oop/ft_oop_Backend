from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import serializers
from rest_framework.response import Response
import requests
import string
import random
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

from .models import UserProfile, GameRoom, MatchHistory, BlockRelation, FriendShip
from .. import settings


class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom

    @transaction.atomic
    def create_game_room(self, user_id, room_name, game_type, room_limit, password):
        if game_type == 'TOURNAMENT':
            type_integer = 1
        elif game_type == 'DUAL':
            type_integer = 0
        else:
            raise serializers.ValidationError('Invalid game type')
        user = get_object_or_404(UserProfile, id=user_id)
        game = GameRoom(room_name=room_name, room_type=type_integer, limits=room_limit, password=password,
                        host=user.user.name)
        user.game_room = game
        game.save()
        user.save()
        return {'game_type': game_type, 'room_id': game.get_room_id()}

    @transaction.atomic
    def exit_game_room(self, user_id, room_id):
        game = get_object_or_404(GameRoom, id=room_id)
        user = UserProfile.objects.get(id=user_id, game_room=game)
        users_in_game = UserProfile.objects.filter(game_room=game)

        if game.get_host() == user.get_user_name():
            for guest in users_in_game:
                guest.game_room = None
                guest.save()
            game.delete()
            return
        user.game_room = None
        user.save()

    @transaction.atomic
    def kick_user_in_game_room(self, room_id, host_name, user_name):
        game = get_object_or_404(GameRoom, id=room_id)
        if game.get_host() != host_name:
            raise serializers.ValidationError("Invalid host name")
        kick_user = get_object_or_404(UserProfile, user_name=user_name)
        kick_user.game_room = None
        kick_user.save()


def get_42oauth_token(code):
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.LOGIN_REDIRECT_URL
    }

    # 기존 front에서 보낸 요청이 아닌, 서버에서 특정 api로 보내는 request
    response = requests.post(settings.FT_TOKEN_URL, data=data)
    print(response.text)
    print(response.status_code)

    if response.status_code == 200:
        ft_access_token = response.json()['access_token']
        return ft_access_token
    else:
        raise Exception(response.json().get('error_description'))


def get_user_info_by_api(ft_access_token):
    headers = {'Authorization': 'Bearer ' + ft_access_token}
    response = requests.get(settings.FT_USER_ATTRIBUTE_URL, headers=headers)
    print(response.text)
    print(response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        return Response('GET User Info from oauth Error', status=response.status_code)


def generate_token(user):
    token = TokenObtainPairSerializer.get_token(user)
    refresh_token = str(token)
    access_token = str(token.access_token)

    return {
        'access': access_token,
        'refresh': refresh_token
    }


@transaction.atomic()
def verify_two_factor_code(code, user_id):
    user = User.objects.filter(id=user_id).first()
    user_profile = UserProfile.objects.get(user_id=user)

    if not user_profile.code == code:
        raise serializers.ValidationError('2fa 코드 불일치')
    user_profile.is_registered = True
    user_profile.save()
    return user


@transaction.atomic
def send_two_factor_code(email, user_id):
    user = UserProfile.objects.get(user_id=user_id)
    code = generate_two_factor_code()
    print(code)
    user.code = code
    user.save()

    subject = "트센 2FA 코드"
    message = f'CODE : {code}'
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [email])


def generate_two_factor_code(length=6):
    characters = string.ascii_uppercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


class UserProfileSerializer(serializers.ModelSerializer):
    game_rooms = GameRoomSerializer(read_only=True, many=True)

    class Meta:
        model = UserProfile
        fields = ['game_rooms', 'picture']

    @transaction.atomic
    def set_nick_name(self, obj, nick_name):
        obj.nick_name = nick_name
        obj.save()

    def is_registered(self, oauth_id):
        try:
            user = User.objects.get(oauth_id=oauth_id)
            return user.is_registered()
        except UserProfile.DoesNotExist:
            return False

    def get_by_email(self, email):
        return get_object_or_404(UserProfile, email=email)

    @transaction.atomic
    def update_user_info(self, user_id, new_name, picture):
        user = get_object_or_404(User, id=user_id)
        if new_name is not None and new_name != "":
            if not User.objects.filter(username=new_name).exists():
                user.username = new_name
                user.save()
            else:
                raise serializers.ValidationError("This nickName is already in use.")
        if picture:
            user.profile.picture = picture
        user.profile.save()


class UserSerializer(serializers.ModelSerializer):
    game_rooms = GameRoomSerializer(source='profile.game_rooms', read_only=True, many=True)
    picture = serializers.CharField(source='profile.picture', read_only=True)
    nick_name = serializers.CharField(source='profile.nick_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'nick_name', 'username', 'email', 'picture', 'game_rooms']

    @transaction.atomic
    def register_user(self, user_info):
        user_name = user_info.get('login')
        picture = user_info['image']['link']
        print('picture ====' + picture)
        email = user_info.get('email')
        oauth_id = user_info.get('id')

        user, user_created = User.objects.get_or_create(username=user_name, defaults={
            'email': email,
        })

        user_profile, profile_created = UserProfile.objects.get_or_create(user=user, defaults={
            'picture': picture,
            'oauth_id': oauth_id,
            'is_registered': False,
        })

        user_profile.picture = picture
        user_profile.oauth_id = oauth_id

        user.save()
        user_profile.save()

        return user


class MatchSerializer(serializers.ModelSerializer):
    winner = serializers.SerializerMethodField()

    class Meta:
        model = MatchHistory
        fields = ['opponent_name', 'winner', 'match_date']

    def get_winner(self, obj):
        if obj.result == 'WIN':
            return obj.user.user_name
        elif obj.result == 'LOSE':
            return obj.opponent_name
        else:
            return None

    def to_representation(self, instance):
        representation = {
            'opponent_name': instance.opponent_name,
            'winner': self.get_winner(instance),
            'match_date': instance.match_date
        }
        return representation


class UserInfoSerializer(serializers.ModelSerializer):
    match_history = MatchSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserProfile
        fields = ['username', 'total_win', 'total_lose', 'match_history', 'picture']


class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['friend']

    def get_friend(self, obj):
        user = obj.friend
        return {'user_name': user.user_name, 'picture': user.picture}

    @transaction.atomic
    def add_friend(self, user_id, friend_name):
        user = get_object_or_404(UserProfile, id=user_id)
        friend = get_object_or_404(UserProfile, user_name=friend_name)
        if not FriendShip.objects.filter(owner=user, friend=friend).exists():
            friend_ship = FriendShip(owner=user, friend=friend)
            friend_ship.save()
        else:
            serializers.ValidationError("Friendship already exists.")

    @transaction.atomic
    def delete_friend(self, user_id, friend_name):
        user = get_object_or_404(User, id=user_id).profile
        friend = get_object_or_404(User, username=friend_name).profile
        friend_ship = get_object_or_404(FriendShip, owner=user, friend=friend)
        friend_ship.delete()


class BlockRelationSerializer(serializers.ModelSerializer):
    blocked = serializers.SerializerMethodField()

    class Meta:
        model = BlockRelation
        fields = ['blocked']

    def get_blocked(self, obj):
        user = obj.blocked
        return {'user_name': user.user_name, 'picture': user.picture}  # 필요한 필드를 선택하여 반환

    @transaction.atomic
    def add_friend_in_ban_list(self, user_id, target):
        user = get_object_or_404(User, id=user_id).profile
        target = get_object_or_404(User, username=target).profile
        if not BlockRelation.objects.filter(blocked=target, blocked_by=user).exists():
            block_relation = BlockRelation(blocked=target, blocked_by=user)
            block_relation.save()
            # 친구 목록에서도 삭제해야할까??
            friend_ship = FriendShip.objects.filter(owner=user, friend=target)
            if friend_ship.exists():
                friend_ship.delete()
        else:
            serializers.ValidationError("Already blocked user.")

    @transaction.atomic
    def remove_friend_in_ban_list(self, user_id, target):
        user = get_object_or_404(User, id=user_id).profile
        target = get_object_or_404(User, username=target).profile
        block_relation = get_object_or_404(BlockRelation, blocked=target, blocked_by=user)
        block_relation.delete()


class MyPageSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    ban_list = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'picture', 'total_win', 'total_lose', 'friends', 'ban_list']

    def get_friends(self, obj):
        friends = FriendShip.objects.filter(owner=obj)
        friend_list = [{'username': f.friend.user.username, 'picture': f.friend.picture} for f in
                       friends]
        return friend_list

    def get_ban_list(self, obj):
        bans = BlockRelation.objects.filter(blocked_by=obj)
        ban_list = [{'username': ban.blocked.user.username, 'picture': ban.blocked.picture} for ban in bans]
        return ban_list


class DualGameRoomSerializer(serializers.ModelSerializer):
    host_picture = serializers.SerializerMethodField()

    class Meta:
        model = GameRoom
        fields = ["host_picture", ]

    def get_host_picture(self, obj):
        host_name = obj.get_host()
        host = UserProfile.objects.filter(user_name=host_name)
        host_picture = host.get_picture()
        return host_picture

    @transaction.atomic
    def enter_dual_room(self, user_id, room_id, password):
        user = get_object_or_404(UserProfile, id=user_id)
        game_room = get_object_or_404(GameRoom, id=room_id)
        if game_room.room_type != 0:
            raise serializers.ValidationError('Invalid Room Type')
        if game_room.limits + 1 < game_room.limits:
            raise serializers.ValidationError('OverFlow limits')
        if game_room.password != password:
            raise serializers.ValidationError('Passwords do not match')
        user.game_room = game_room
        user.save()
        host = get_object_or_404(UserProfile, user_name=game_room.get_host())
        return {"hostPicture": host.picture()}


class TournamentRoomSerializer(serializers.ModelSerializer):
    host_name = serializers.SerializerMethodField()
    host_picture = serializers.SerializerMethodField()
    guest_list = serializers.SerializerMethodField()

    class Meta:
        model = GameRoom
        fields = ["host_name", "host_picture", "guest_list", ]

    def get_host_name(self, obj):
        return obj.get_host()

    def get_host_picture(self, obj):
        host_name = obj.get_host()
        host = UserProfile.objects.filter(user_name=host_name)
        host_picture = host.get_picture()
        return host_picture

    def get_guest_list(self, obj):
        users = UserProfile.objects.filter(game_room=obj)
        guest_list = [{'nic_name': user.get_nick_name(), 'picture': user.get_picture()} for user in users]
        return guest_list

    def enter_tournament_room(self, nick_name, user_id, password, room_id):
        game_room = get_object_or_404(GameRoom, id=room_id)
        users_in_game = UserProfile.objects.filter(game_room=game_room)
        if game_room.room_type != 1:
            raise serializers.ValidationError("Invalid Room Type")
        if game_room.password != password:
            raise serializers.ValidationError("Passwords do not match")
        if users_in_game.count() + 1 > game_room.limits:
            raise serializers.ValidationError("Limits exceeded")
        user = get_object_or_404(UserProfile, id=user_id)
        user.nick_name = nick_name
        user.game_room = game_room

        host_picture = get_object_or_404(UserProfile, user_name=game_room.get_host()).get_picture()
        guest_list = self.get_guest_list(game_room)
        user.save()

        return {"host_name": game_room.get_host(), "host_picture": host_picture, "guest_list": guest_list}


def get_user_info_from_token(request):
    header = request.META.get("HTTP_AUTHORIZATION")
    token_str = header.split('Bearer ')[1]
    token = AccessToken(token_str)

    return token['user_id']
