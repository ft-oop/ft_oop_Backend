import json

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serializer import UserInfoSerializer, UserSerializer, MatchSerializer, MyPageSerializer, DualGameRoomSerializer, \
    TournamentRoomSerializer, GameRoomSerializer, FriendSerializer, BlockRelationSerializer, get_user_info_by_api, \
    get_42oauth_token, generate_token, send_two_factor_code, verify_two_factor_code
from .models import User, BlockRelation, MatchHistory, FriendShip, GameRoom
from django.http import HttpResponse, JsonResponse


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def login(request):
    serializer = UserSerializer(data=request.data)
    code = request.GET.get('code', '')
    access_token = get_42oauth_token(code)
    user_info = get_user_info_by_api(access_token)
    user = serializer.register_user(user_info=user_info)

    if not user.is_registered:
        return JsonResponse(user_info['email'], safe=False, status=status.HTTP_201_CREATED)
    return JsonResponse(generate_token(user), safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
def reissue_access_token(request):
    serializer = TokenRefreshSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def send_email(request):
    email = request.GET.get('email')
    print(email)
    send_two_factor_code(email)
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
def two_factor(request):
    serializer = UserSerializer(data=request.data)
    code = request.data['two_factor_code']
    email = request.data['email']
    verify_two_factor_code(code, email)
    user = serializer.get_by_email(email)
    return JsonResponse(generate_token(user), status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_user(request):
    intra_name = request.GET.get('intra_name')
    print(intra_name)
    try:
        user = get_object_or_404(User, intra_name=intra_name)
    except RuntimeError:
        return HttpResponse(status=404, message="User Not Found")

    serializer = UserSerializer(user, many=False)
    return JsonResponse(serializer.data, safe=False, status=200)


@api_view(['GET'])
def get_user_info(request):
    intra_name = request.GET.get('intra_name')
    user_name = request.GET.get('user')

    try:
        me = get_object_or_404(User, intra_name=intra_name)
    except RuntimeError:
        return HttpResponse(status=404, message="User Not Found")
    try:
        find_user = get_object_or_404(User, intra_name=user_name)
    except RuntimeError:
        return HttpResponse(status=404, message="User Not Found")
    blocked = BlockRelation.objects.filter(blocked_by=me, blocked=find_user)
    is_blocked = blocked.exists()

    user_info = UserInfoSerializer(find_user).data
    user_info['is_block'] = is_blocked
    return JsonResponse(user_info, safe=False, status=200)


@api_view(['GET'])
def get_my_page(request):
    try:
        user = get_object_or_404(User, intra_name=request.GET.get('intra_name'))
    except RuntimeError:
        return HttpResponse(status=404, message="User Not Found")
    my_page_dto = MyPageSerializer(user).data

    return JsonResponse(my_page_dto, safe=False, status=200)


@api_view(['GET'])
def enter_dual_room(request, room_id):
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')
    service = DualGameRoomSerializer()
    data = service.enter_dual_room(user_name, room_id, password)

    return JsonResponse(data, safe=False, status=200)


@api_view(['GET'])
def enter_tournament_room(request, tournament_id):
    nick_name = request.GET.get('nick_name')
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')

    service = TournamentRoomSerializer()
    data = service.enter_tournament_room(nick_name, user_name, password, tournament_id)

    return JsonResponse(data, safe=False, status=200)


@api_view(['POST'])
def create_game(request):
    try:
        data = json.loads(request.body)
        room_name = data['room_name']
        game_type = data['game_type']
        room_limit = data['room_limit']
        password = data['password']
        user_name = data['user_name']
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
    user_name = request.GET.get('user_name')
    service = GameRoomSerializer()
    service.exit_game_room(user_name, room_id)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def kick_user_in_game_room(request, room_id):
    try:
        data = json.loads(request.body)
        host_name = data['host_name']
        kick_user = data['kick_user']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    service = GameRoomSerializer()
    service.kick_user_in_game_room(room_id, host_name, kick_user)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def edit_my_page(request):
    try:
        data = json.loads(request.body)
        user_name = data['user_name']
        nick_name = data['nick_name']
        picture = data['picture']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    servie = UserSerializer()
    servie.update_user_info(user_name, nick_name, picture)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def add_friend(request):
    try:
        data = json.loads(request.body)
        user_name = data['user_name']
        friend = data['friend']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)

    service = FriendSerializer()
    service.add_friend(user_name, friend)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['DELETE'])
def delete_friend(request):
    try:
        data = json.loads(request.body)
        user_name = data['user_name']
        friend = data['friend']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    service = FriendSerializer()
    service.delete_friend(user_name, friend)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def add_friend_in_ban_list(request):
    try:
        data = json.loads(request.body)
        user_name = data['user_name']
        target = data['target']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    service = BlockRelationSerializer()
    service.add_friend_in_ban_list(user_name, target)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['DELETE'])
def remove_friend_in_ban_list(request):
    try:
        data = json.loads(request.body)
        user_name = data['user_name']
        target = data['target']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    service = BlockRelationSerializer()
    service.remove_friend_in_ban_list(user_name, target)
    return JsonResponse('OK', safe=False, status=200)
