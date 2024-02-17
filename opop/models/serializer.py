from turtledemo.sorting_animate import Block

from rest_framework import serializers

from .models import User, GameRoom, MatchHistory, BlockRelation, FriendShip


class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom


class UserSerializer(serializers.ModelSerializer):
    game_rooms = GameRoomSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'intra_name', 'picture', 'game_rooms']


class MatchSerializer(serializers.ModelSerializer):
    winner = serializers.SerializerMethodField()

    class Meta:
        model = MatchHistory
        fields = ['opponent_name', 'winner', 'match_date']

    def get_winner(self, obj):
        if obj.result == 'WIN':
            return obj.user.intra_name
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
        fields = ['total_win', 'total_lose', 'match_history',]


class FrindDto(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['friend']

    def get_friend(self, obj):
        user = obj.friend
        return {'intra_name': user.intra_name, 'picture': user.picture}


class BlockRelationSerializer(serializers.ModelSerializer):
    blocked = serializers.SerializerMethodField()

    class Meta:
        model = BlockRelation
        fields = ['blocked']

    def get_blocked(self, obj):
        user = obj.blocked
        return {'intra_name': user.intra_name, 'picture': user.picture}  # 필요한 필드를 선택하여 반환


class MyPageSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    ban_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['intra_name', 'picture', 'total_win', 'total_lose', 'friends', 'ban_list']

    def get_friends(self, obj):
        friends = FriendShip.objects.filter(owner=obj)
        friend_list = [{'intra_name': friend.friend.intra_name, 'picture': friend.friend.picture} for friend in
                       friends]
        return friend_list

    def get_ban_list(self, obj):
        bans = BlockRelation.objects.filter(blocked_by=obj)
        ban_list = [{'intra_name': ban.blocked.intra_name, 'picture': ban.blocked.picture} for ban in bans]
        return ban_list

