from django.contrib import admin
from .models import User, GameRoom, MatchHistory, FriendShip, BlockRelation, Message

admin.site.register(User)
admin.site.register(GameRoom)
admin.site.register(Message)
admin.site.register(MatchHistory)
admin.site.register(FriendShip)
admin.site.register(BlockRelation)
