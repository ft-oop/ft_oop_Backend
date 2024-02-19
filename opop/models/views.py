import json

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from .serializer import UserInfoSerializer, UserSerializer, MatchSerializer, MyPageSerializer, DualGameRoomSerializer, \
    TournamentRoomSerializer, GameRoomSerializer, FriendSerializer, BlockRelationSerializer
from .models import User, BlockRelation, MatchHistory, FriendShip, GameRoom
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from json.decoder import JSONDecodeError


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)


@api_view(['GET'])
def get_user(request):
    intra_name = request.GET.get('intra_name')
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
    try:
        game_room = get_object_or_404(GameRoom, id=room_id)
    except RuntimeError:
        return HttpResponse(status=404, message="game room Not Found")
    dual_room_dto = DualGameRoomSerializer(game_room).data

    return JsonResponse(dual_room_dto, safe=False, status=200)


@api_view(['GET'])
def enter_tournament_room(request, tournament_id):
    nick_name = request.GET.get('nick_name')
    user_name = request.GET.get('user_name')

    try:
        user = get_object_or_404(User, intra_name=user_name)
    except RuntimeError:
        return HttpResponse(status=404, message="User Not Found")
    UserSerializer.set_nick_name(user, nick_name)

    try:
        game_room = get_object_or_404(GameRoom, id=tournament_id)
    except RuntimeError:
        return HttpResponse(status=404, message="game room Not found")
    tournament_room_dto = TournamentRoomSerializer(game_room).data

    return JsonResponse(tournament_room_dto, safe=False, status=200)


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

    try:
        response = GameRoomSerializer.create_game_room(user_name, room_name, game_type, room_limit, password)
    except ValidationError as e:
        return JsonResponse(e.detail, status=400)
    return JsonResponse(response, safe=False, status=200)


@api_view(['POST'])
def exit_game_room(request, room_id):
    user_name = request.GET.get('userName')
    GameRoomSerializer.exit_game_room(user_name, room_id)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def kick_user_in_game_room(request, room_id):
    try:
        data = json.loads(request.body)
        host_name = data['host_name']
        kick_user = data['kick_user']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    try:
        GameRoomSerializer.kick_user_in_game_room(room_id, host_name, kick_user)
    except ValidationError as e:
        return JsonResponse(e.detail, status=404)
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
    UserSerializer.update_user_info(user_name, nick_name, picture)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def add_friend(request):
    try:
        data = json.loads(request.body)
        user_name = data['user_name']
        friends = data['friends']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    FriendSerializer.add_friends(user_name, friends)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def delete_friend(request):
    try:
        data = json.loads(request.body)
        user_name = data['user_name']
        friends = data['friends']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    FriendSerializer.delete_friends(user_name, friends)


@api_view(['POST'])
def add_friend_in_ban_list(request):
    try:
        data = json.loads(request.body)
        user_name = data['user_name']
        target = data['target']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    BlockRelationSerializer.add_friend_in_ban_list(user_name, target)
    return JsonResponse('OK', safe=False, status=200)


@api_view(['POST'])
def remove_friend_in_ban_list(request):
    try:
        data = json.loads(request.body)
        user_name = data['user_name']
        target = data['target']
    except KeyError:
        return JsonResponse({'error': 'Bad Request'}, status=400)
    BlockRelationSerializer.remove_friend_in_ban_list(user_name, target)
    return JsonResponse('OK', safe=False, status=200)