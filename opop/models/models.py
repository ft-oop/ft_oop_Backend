from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class GameRoom(models.Model):
    id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=64)
    room_type = models.IntegerField(default=0)
    limits = models.IntegerField(default=0)
    password = models.CharField(max_length=12)
    host = models.CharField(max_length=10)

    def __str__(self):
        return self.room_name

    def get_room_id(self):
        return self.id

    def get_room_name(self):
        return self.room_name

    def get_room_type(self):
        return self.room_type

    def get_limits(self):
        return self.limits

    def get_pass_word(self):
        return self.password

    def get_host(self):
        return self.host

    def get_user(self):
        user_info = []
        for user in self.users.all():
            user_info.append({
                'username' : user.user.username,
            })
        return user_info


    
    def get_room_person(self):
        return len(self.users.all())


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id = models.AutoField(primary_key=True)

    oauth_id = models.IntegerField(default=0)
    nick_name = models.CharField(max_length=15, default='')

    total_win = models.IntegerField(default=0)
    total_lose = models.IntegerField(default=0)
    code = models.CharField(max_length=6, default='')
    game_room = models.ForeignKey(GameRoom, on_delete=models.SET_NULL, null=True, related_name='users')

    # User 정보에서 이동
    picture = models.TextField()
    is_registered = models.BooleanField(default=False)
    on_line = models.BooleanField(default=False)

    def get_picture(self):
        return self.picture

    def get_total_win(self):
        return self.total_win

    def get_total_lose(self):
        return self.total_lose

    def get_is_registered(self):
        return self.is_registered

    def get_nick_name(self):
        return self.nick_name



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class MatchHistory(models.Model):
    id = models.AutoField(primary_key=True)
    opponent_name = models.CharField(max_length=10)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='match_history')
    result = models.CharField(max_length=10)
    game_type = models.CharField(max_length=10)
    match_date = models.DateField()

    def __str__(self):
        return f"{self.user.user_name} vs. {self.opponent_name} - {self.result}"

    def get_opponent_name(self):
        return self.opponent_name

    def get_date(self):
        return self.match_date

    def get_game_type(self):
        return self.game_type

    def get_result(self):
        return self.result


class FriendShip(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(UserProfile, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(UserProfile, related_name='friends', on_delete=models.CASCADE)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class BlockRelation(models.Model):
    blocked = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blocked_by_relations')
    blocked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blocking_relations')
