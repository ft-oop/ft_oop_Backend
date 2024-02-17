from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    intra_name = models.CharField(max_length=10)
    picture = models.CharField(max_length=255)
    total_win = models.IntegerField(default=0)
    total_lose = models.IntegerField(default=0)
    email = models.EmailField()
    game_room = models.ForeignKey('GameRoom', on_delete=models.SET_NULL, null=True, related_name='users')

    def __str__(self):
        return self.intra_name

    def get_intra_name(self):
        return self.intra_name

    def get_picture(self):
        return self.picture

    def get_total_win(self):
        return self.total_win

    def get_total_lose(self):
        return self.total_lose

    def get_email(self):
        return self.email


class BlockRelation(models.Model):
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by_relations')
    blocked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking_relations')


class GameRoom(models.Model):
    id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=64)
    room_type = models.IntegerField(default=0)
    limits = models.IntegerField(default=0)
    passWord = models.CharField(max_length=12)
    host = models.CharField(max_length=10)

    def __str__(self):
        return self.room_name

    def get_room_name(self):
        return self.room_name

    def get_room_type(self):
        return self.room_type

    def get_limits(self):
        return self.limits

    def get_pass_word(self):
        return self.passWord

    def get_host(self):
        return self.host

    def get_user(self):
        return list(self.users.all())


class MatchHistory(models.Model):
    id = models.AutoField(primary_key=True)
    opponent_name = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_history')
    result = models.CharField(max_length=10)
    game_type = models.CharField(max_length=10)
    match_date = models.DateField()

    def __str__(self):
        return f"{self.user.intra_name} vs. {self.opponent_name} - {self.result}"

    def get_opponent_name(self):
        return self.opponent_name

    def get_date(self):
        return self.match_date

    def get_game_type(self):
        return self.game_type

    def get_result(self):
        return self.result


class FriendShip(models.Model):
    owner = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)