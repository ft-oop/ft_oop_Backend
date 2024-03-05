from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate_header(self, request):
        # 누락된 Bearer 토큰에 대해 사용자 정의 헤더 반환
        return 'Bearer realm="api"'

    def authenticate(self, request):
        print('path = ' + request.path)
        if request.path == '/oauth/login/' or request.path == '/jwt/reissue':
            return None

        raw_token = request.META.get('HTTP_AUTHORIZATION', None)
        if not raw_token:
            # 토큰이 누락된 경우 403 오류 반환
            raise exceptions.PermissionDenied('No credentials provided.')

        return super().authenticate(request)
