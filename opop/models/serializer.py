from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import serializers

from .models import User, GameRoom, MatchHistory, BlockRelation, FriendShip


class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom

    @transaction.atomic
    def create_game_room(self, user_name, room_name, game_type, room_limit, password):
        if game_type == 'TOURNAMENT':
            type_integer = 1
        elif game_type == 'DUAL':
            type_integer = 0
        else:
            raise serializers.ValidationError('Invalid game type')
        user = get_object_or_404(User, user_name=user_name)
        game = GameRoom(room_name=room_name, room_type=type_integer, limits=room_limit, password=password, host=user.get_intra_name())
        user.game_room = game
        game.save()
        user.save()
        return {'game_type': game_type, 'room_id': game.get_room_id()}

    @transaction.atomic
    def exit_game_room(self, user_name, room_id):
        game = get_object_or_404(GameRoom, id=room_id)
        user = User.objects.get(user_name=user_name, game_room=game)
        users_in_game = User.objects.filter(game_room=game)

        if game.get_host() == user.get_intra_name():
            for guest in users_in_game:
                guest.game_room = None
                guest.save()
            game.delete()
            return
        user.game_room = None
        user.save()

        if users_in_game.count() == 0:
            game.delete()

    @transaction.atomic
    def kick_user_in_game_room(self, room_id, host_name, user_name):
        game = get_object_or_404(GameRoom, id=room_id)
        if game.get_host() != host_name:
            raise serializers.ValidationError("Invalid host name")
        kick_user = get_object_or_404(User, user_name=user_name)
        kick_user.game_room = None
        kick_user.save()


class UserSerializer(serializers.ModelSerializer):
    game_rooms = GameRoomSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'user_name', 'picture', 'game_rooms']

    @transaction.atomic
    def set_nick_name(self, obj, nick_name):
        obj.nick_name = nick_name
        obj.save()

    @transaction.atomic
    def update_user_info(self, user_name, nick_name, picture):
        user = get_object_or_404(User, user_name=user_name)
        if nick_name is not None:
            user.nick_name = nick_name
        if picture is not None:
            user.picture = picture
        user.save()


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

    class Meta:
        model = User
        fields = ['total_win', 'total_lose', 'match_history', ]


class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['friend']

    def get_friend(self, obj):
        user = obj.friend
        return {'user_name': user.user_name, 'picture': user.picture}

    @transaction.atomic
    def add_friend(self, user_name, friend_name):
        user = get_object_or_404(User, user_name=user_name)
        friend = get_object_or_404(User, user_name=friend_name)
        friend_ship = FriendShip(owner=user, friend=friend)
        friend_ship.save()

    @transaction.atomic
    def delete_friend(self, user_name, friend_name):
        user = get_object_or_404(User, user_name=user_name)
        friend = get_object_or_404(User, user_name=friend_name)
        friend_ship = FriendShip.objects.get(owner=user, friend=friend)
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
    def add_friend_in_ban_list(self, user_name, target):
        user = get_object_or_404(User, user_name=user_name)
        target = get_object_or_404(User, user_name=target)
        block_relation = BlockRelation(blocked=target, blocked_by=user)
        block_relation.save()
        # 친구 목록에서도 삭제해야할까??

    @transaction.atomic
    def remove_friend_in_ban_list(self, user_name, target):
        user = get_object_or_404(User, user_name=user_name)
        target = get_object_or_404(User, user_name=target)
        block_relation = get_object_or_404(BlockRelation, blocked=target, blocked_by=user)
        block_relation.delete()


class MyPageSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    ban_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_name', 'picture', 'total_win', 'total_lose', 'friends', 'ban_list']

    def get_friends(self, obj):
        friends = FriendShip.objects.filter(owner=obj)
        friend_list = [{'user_name': friend.friend.user_name, 'picture': friend.friend.picture} for friend in
                       friends]
        return friend_list

    def get_ban_list(self, obj):
        bans = BlockRelation.objects.filter(blocked_by=obj)
        ban_list = [{'user_name': ban.blocked.user_name, 'picture': ban.blocked.picture} for ban in bans]
        return ban_list


class DualGameRoomSerializer(serializers.ModelSerializer):
    host_picture = serializers.SerializerMethodField()

    class Meta:
        model = GameRoom
        fields = ["host_picture", ]

    def get_host_picture(self, obj):
        host_name = obj.get_host()
        host = User.objects.filter(user_name=host_name)
        host_picture = host.get_picture()
        return host_picture

    @transaction.atomic
    def enter_dual_room(self, user_name, room_id, password):
        user = get_object_or_404(User, user_name=user_name)
        game_room = get_object_or_404(GameRoom, id=room_id)
        if game_room.room_type != 0:
            raise serializers.ValidationError('Invalid Room Type')
        if game_room.limits  + 1 < game_room.limits:
            raise serializers.ValidationError('OverFlow limits')
        if game_room.password != password:
            raise serializers.ValidationError('Passwords do not match')
        user.game_room = game_room
        user.save()
        host = get_object_or_404(User, user_name=game_room.get_host())
        return {"hostPicture": host.get_picture()}


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
        host = User.objects.filter(user_name=host_name)
        host_picture = host.get_picture()
        return host_picture

    def get_guest_list(self, obj):
        users = User.objects.filter(game_room=obj)
        guest_list = [{'nic_name': user.get_nick_name(), 'picture': user.get_picture()} for user in users]
        return guest_list

    def enter_tournament_room(self, nick_name, user_name, password, room_id):
        game_room = get_object_or_404(GameRoom, id=room_id)
        if game_room.room_type != 1:
            raise serializers.ValidationError("Invalid Room Type")
        if game_room.password != password:
            raise serializers.ValidationError("Passwords do not match")
        if game_room.limits + 1 > game_room.limits:
            raise serializers.ValidationError("Limits exceeded")
        user = get_object_or_404(User, username=user_name)
        user.nick_name = nick_name
        user.game_room = game_room

        host_picture = get_object_or_404(User, user_name=game_room.get_host()).get_picture()
        guest_list = self.get_guest_list(game_room)
        user.save()

        return {"host_name": game_room.get_host(), "host_picture": host_picture, "guest_list": guest_list}

