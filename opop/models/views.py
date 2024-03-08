import json

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serializer import UserInfoSerializer, UserProfileSerializer, MatchSerializer, MyPageSerializer, \
    DualGameRoomSerializer, \
    TournamentRoomSerializer, GameRoomSerializer, FriendSerializer, BlockRelationSerializer, get_user_info_by_api, \
    get_42oauth_token, generate_token, send_two_factor_code, verify_two_factor_code, get_user_info_from_token, \
    UserSerializer
from .models import UserProfile, BlockRelation, MatchHistory, FriendShip, GameRoom
from django.http import HttpResponse, JsonResponse


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    serializer = UserSerializer(data=request.data)
    code = request.data['code']
    access_token = get_42oauth_token(code)
    user_info = get_user_info_by_api(access_token)
    user = serializer.register_user(user_info=user_info)

    if not user.profile.is_registered:
        return JsonResponse(generate_token(user), safe=False, status=status.HTTP_201_CREATED)
    return JsonResponse(generate_token(user), safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def reissue_access_token(request):
    print('재발급 요청 실행')
    serializer = TokenRefreshSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def send_email(request):
    user_id = get_user_info_from_token(request)
    email = get_object_or_404(User, id=user_id).email
    send_two_factor_code(email, user_id)
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
def two_factor(request):
    user_id = get_user_info_from_token(request)
    code = request.data['code']
    user = verify_two_factor_code(code, user_id)
    return JsonResponse(generate_token(user), status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_users(request):
    users = UserProfile.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)


@api_view(['GET'])
def get_user(request):
    user_id = get_user_info_from_token(request)
    try:
        user = get_object_or_404(User, id=user_id)
    except RuntimeError:
        return HttpResponse(status=404, message="User Not Found")

    serializer = UserSerializer(user, many=False)
    return JsonResponse(serializer.data, safe=False, status=200)


@api_view(['GET'])
def get_user_info(request):
    user_id = get_user_info_from_token(request)
    user_name = request.GET.get('userName')
    try:
        me = get_object_or_404(User, id=user_id).profile
    except RuntimeError:
        return HttpResponse(status=404, message="User Not Found")
    try:
        find_user = get_object_or_404(User, username=user_name).profile
    except RuntimeError:
        return HttpResponse(status=404, message="User Not Found")
    blocked = BlockRelation.objects.filter(blocked_by=me, blocked=find_user)
    is_blocked = blocked.exists()

    user_info = UserInfoSerializer(find_user).data
    user_info['is_block'] = is_blocked
    return JsonResponse(user_info, safe=False, status=200)


@api_view(['GET'])
def get_my_page(request):
    user_id = get_user_info_from_token(request)
    try:
        user = get_object_or_404(User, id=user_id).profile
    except RuntimeError:
        return HttpResponse(status=404, message="User Not Found")
    my_page_dto = MyPageSerializer(user).data
    return JsonResponse(my_page_dto, safe=False, status=200)


@api_view(['GET'])
def enter_dual_room(request, room_id):
    user_name = request.GET.get('userName')
    password = request.GET.get('password')
    service = DualGameRoomSerializer()
    data = service.enter_dual_room(user_name, room_id, password)

    return JsonResponse(data, safe=False, status=200)


@api_view(['GET'])
def enter_tournament_room(request, tournament_id):
    nick_name = request.GET.get('nickName')
    user_name = request.GET.get('userName')
    password = request.GET.get('password')

    service = TournamentRoomSerializer()
    data = service.enter_tournament_room(nick_name, user_name, password, tournament_id)

    return JsonResponse(data, safe=False, status=200)


@api_view(['POST'])
def create_game(request):
    try:
        data = json.loads(request.body)
        room_name = data['roomName']
        game_type = data['gameType']
        room_limit = data['roomLimit']
        password = data['password']
        user_name = data['userName']
    except KeyError:
        return JsonResponse({'message': 'Bad Request'}, status=400)
    service = GameRoomSerializer()
    try:
        response = service.create_game_room(user_name, room_name, game_type, room_limit, password)
    except ValidationError as e:
        return JsonResponse(e.detail, status=400)
    return JsonResponse(response, safe=False, status=200)


@api_view(['POST'])
def exit_game_room(request, room_id):
    user_name = request.GET.get('userName')
    service = GameRoomSerializer()
    service.exit_game_room(user_name, room_id)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def kick_user_in_game_room(request, room_id):
    try:
        data = json.loads(request.body)
        host_name = data['hostName']
        kick_user = data['kickUser']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    service = GameRoomSerializer()
    service.kick_user_in_game_room(room_id, host_name, kick_user)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def edit_my_page(request):
    user_id = get_user_info_from_token(request)
    try:
        data = json.loads(request.body)
        new_name = data['newName']
        picture = data['picture']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    servie = UserProfileSerializer()
    servie.update_user_info(user_id, new_name, picture)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def add_friend(request):
    try:
        data = json.loads(request.body)
        user_name = data['userName']
        friend = data['friend']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)

    service = FriendSerializer()
    service.add_friend(user_name, friend)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def delete_friend(request):
    user_id = get_user_info_from_token(request)
    try:
        data = json.loads(request.body)
        friend = data['friendName']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    service = FriendSerializer()
    service.delete_friend(user_id, friend)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def add_friend_in_ban_list(request):
    user_id = get_user_info_from_token(request)
    try:
        data = json.loads(request.body)
        target = data['blockName']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    service = BlockRelationSerializer()
    service.add_friend_in_ban_list(user_id, target)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def remove_friend_in_ban_list(request):
    user_id = get_user_info_from_token(request)
    try:
        data = json.loads(request.body)
        target = data['blockName']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    service = BlockRelationSerializer()
    service.remove_friend_in_ban_list(user_id, target)
    return JsonResponse('OK', safe=False, status=200)
