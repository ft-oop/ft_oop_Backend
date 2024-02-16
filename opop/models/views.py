from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializer import UserSerializer
from .models import User
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser


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
