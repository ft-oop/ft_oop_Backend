from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate_header(self, request):
        return 'Bearer realm="api"'

    def authenticate(self, request):
        print('path = ' + request.path)
        if request.path == '/api/oauth/login/' or request.path == '/api/jwt/reissue':
            return None

        raw_token = request.META.get('HTTP_AUTHORIZATION', None)
        if not raw_token:
            raise exceptions.PermissionDenied('No credentials provided.')

        return super().authenticate(request)
