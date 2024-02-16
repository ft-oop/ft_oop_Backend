from rest_framework import serializers

from .models import User, GameRoom, MatchHistory, BlockRelation


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
            print(obj.user.intra_name)
            return obj.user.intra_name
        elif obj.result == 'LOSE':
            print(obj.opponent_name)
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
        fields = ['total_win', 'total_lose', 'match_history']


class FrindDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fileds = ['id', 'username']