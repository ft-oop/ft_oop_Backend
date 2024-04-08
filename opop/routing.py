# from django.urls import re_path

# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/main/$', consumers.MainConsumer.as_asgi()),
# ]
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/main/', consumers.NoticeConsumer.as_asgi()),
    path('ws/main/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi())
]