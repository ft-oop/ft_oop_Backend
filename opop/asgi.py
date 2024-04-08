import os

# Django 설정 로드 전에 설정 파일 경로를 환경 변수에 설정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opop.settings')

from django.core.asgi import get_asgi_application
# Django 설정을 로드합니다.
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .jwt_middleware import JWTAuthMiddleware
import opop.routing

# ASGI 프로토콜에 따라 요청을 처리하는 핸들러를 설정합니다.
application = ProtocolTypeRouter({
    # 'http': django_asgi_app,
    # 'websocket': AuthMiddlewareStack(
    #     URLRouter(
    #         opop.routing.websocket_urlpatterns
    #     )
    # ),
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        JWTAuthMiddleware(
            URLRouter(
                opop.routing.websocket_urlpatterns
                )
        )
    ),
})
