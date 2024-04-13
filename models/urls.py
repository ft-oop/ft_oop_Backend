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
    path('mypage/friend', views.add_friend),
    path('game/dual/<int:room_id>', views.enter_dual_room),
    path('game/tournament/<int:room_id>', views.enter_tournament_room),
    path('game/tournament/nickname', views.set_host_nick_name),
    path('game', views.create_game),
    path('game/<int:room_id>/exit', views.exit_game_room),
    # path('game/<int:room_id>/dual/kick', views.kick_user_in_dual_room),
    path('game/<int:room_id>/tournament/kick', views.kick_user_in_tournament_room),
    path('friend/add', views.add_friend),
    path('friend/delete', views.delete_friend),
    path('friend/ban-list/add', views.add_friend_in_ban_list),
    path('friend/ban-list/delete', views.remove_friend_in_ban_list),
    path('mypage/chat', views.get_chat_history),

    # 로그인 로직 
    path('oauth/login/', views.login),
    path('oauth/login/2FA', views.two_factor),
    path('oauth/login/2FA/email', views.send_email),
    path('jwt/reissue', views.reissue_access_token),
]
