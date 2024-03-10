from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/main/', consumers.GameConsumer.as_asgi()),
]
