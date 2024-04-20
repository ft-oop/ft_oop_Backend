from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/main/', consumers.NoticeConsumer.as_asgi()),
    path('ws/main/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('ws/main/game/<str:room_name>/', consumers.GameConsumer.as_asgi()),
    path('ws/main/tournament/<str:room_name>/', consumers.TournamentConsumer.as_asgi())
]