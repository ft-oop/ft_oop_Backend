import json

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializer import UserInfoSerializer, UserSerializer, MatchSerializer, MyPageSerializer
from .models import User, BlockRelation, MatchHistory, FriendShip
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from json.decoder import JSONDecodeError

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    return HttpResponse(status=404, message="Not Found")


@api_view(['GET'])
def get_user(request):
    # if request.method == 'GET':
    intra_name = request.GET.get('intra_name')
    user = get_object_or_404(User, intra_name=intra_name)
    serializer = UserSerializer(user, many=False)
    return JsonResponse(serializer.data, safe=False)
    # return HttpResponse(status=404, message="Not Found")


@api_view(['GET'])
def get_user_info(request):
    intra_name = request.GET.get('intra_name')
    user_name = request.GET.get('user')

    me = get_object_or_404(User, intra_name=intra_name)
    find_user = get_object_or_404(User, intra_name=user_name)
    blocked = BlockRelation.objects.filter(blocked_by=me, blocked=find_user)
    is_blocked = blocked.exists()

    user_info = UserInfoSerializer(find_user).data
    user_info['is_block'] = is_blocked
    return JsonResponse(user_info, safe=False)


@api_view(['GET'])
def get_my_page(request):
    user = get_object_or_404(User, intra_name=request.GET.get('intra_name'))
    my_page_dto = MyPageSerializer(user).data

    return JsonResponse(my_page_dto, safe=False)
