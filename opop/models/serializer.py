from rest_framework import serializers

from .models import User, GameRoom


class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom


class UserSerializer(serializers.ModelSerializer):
    gameRooms = GameRoomSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ['id', 'intra_name', 'gameRooms']


class FrindDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fileds = ['id', 'username']