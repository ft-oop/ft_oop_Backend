from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register('User', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('allUsers/', views.get_all_users),
    path('main/', views.get_user),
    path('users/info/', views.get_user_info),
    path('mypage/', views.get_my_page)
]
