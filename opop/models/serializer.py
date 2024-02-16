from rest_framework import serializers

from .models import User, GameRoom, MatchHistory


class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom


class UserSerializer(serializers.ModelSerializer):
    gameRooms = GameRoomSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'intra_name', 'picture', 'gameRooms']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchHistory
        fields = ['opponent_name', 'winner']

    def get_winner(self, obj):
        if obj.result == 'WIN':
            return obj.user.intra_name
        elif obj.result == 'LOSE':
            return obj.opponent_name.intra_name
        else:
            return None

    def to_representation(self, instance):
        representation = {
            'opponent_name': instance.opponet_name,
            'winner': self.get_winner(instance)
        }
        return representation


class UserInfoSerializer(serializers.ModelSerializer):

    gameRooms = GameRoomSerializer(read_only=True, many=True)
    matchHistory = MatchSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['total_win', 'total_lose', 'isBlack', 'matchHistory']


class FrindDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fileds = ['id', 'username']