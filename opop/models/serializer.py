from rest_framework import serializers

from .models import User

class FrindDto(serializers.ModelSerializer):
    class Meta:
        model = User
        fileds = ['id', 'username']