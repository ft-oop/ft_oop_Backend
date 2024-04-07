from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from .models.models import UserProfile
from django.contrib.auth.models import User
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        # try:
        jwt_token = await self.get_jwt_token(scope)
        user = await self.get_user_info_from_token(jwt_token)
        scope['user'] = user
        # except Exception as e:
        #     scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)

    async def get_jwt_token(self, scope):
        jwt_token = None
        headers = dict(scope['headers'])
        if b'cookie' in headers:
            cookies = headers[b'cookie'].decode()
            cookie_list = cookies.split('; ')
            for cookie in cookie_list:
                name, value = cookie.split('=')
                if name == 'jwt':
                    jwt_token = value
        return jwt_token

    @database_sync_to_async
    def get_user_info_from_token(self, jwt):
        try:
            token = AccessToken(jwt)
            user_id = token['user_id']
            user = User.objects.get(id=user_id)

            return user.profile
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'User does not exist'

            }, status=404)
