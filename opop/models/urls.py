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
    path('mypage/', views.get_my_page),
    path('mypage/editor', views.edit_my_page),
    path('game/dual/<int:room_id>', views.enter_dual_room),
    path('game/tournament/<int:room_id>', views.enter_tournament_room),
    path('game', views.create_game),
    path('game/<int:room_id>/exit', views.exit_game_room),
    path('game/<int:room_id>/kick', views.kick_user_in_game_room),
    path('friend/add', views.add_friend),
    path('friend/delete', views.delete_friend),
    path('friend/ban-list/add', views.add_friend_in_ban_list),
    path('friend/ban-list/delete', views.remove_friend_in_ban_list),

    # 로그인 로직 
    path('login', views.login),
    path('2FA', views.two_factor),
    path('2FA/email', views.send_email)
]
