from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/main/', consumers.OopConsumer.as_asgi()),
]
