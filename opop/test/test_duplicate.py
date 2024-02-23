from django.test import TestCase
from opop.models.models import User, FriendShip
import json

class UserBlockRelationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            intra_name='sohyupar',
            picture='testtestpic',
            nick_name='nick1',
            total_win=0,
            total_lose=0,
            email='test@ettt.com',
        )

        self.user2 = User.objects.create(
            intra_name='jinoh',
            picture='testtestpic',
            nick_name='nick2',
            total_win=0,
            total_lose=0,
            email='test@ettt.com',
        )

        self.user3 = User.objects.create(
            intra_name='suhwpark',
            picture='testtestpic',
            nick_name='nick3',
            total_win=0,
            total_lose=0,
            email='test@ettt.com',
        )

    def test_duplicate_nick(self):
        print("Nick before  :", self.user2.nick_name)

        data = {
            'user_name':    'jinoh',
            'nick_name':    'nick4',
            'picture':      'pic2'
        }
        self.client.post('/mypage/editor', json.dumps(data), content_type='application/json')
        print("Nick After   :", User.objects.get(intra_name='jinoh').nick_name)

        print("Nick before  :", self.user3.nick_name)

        data = {
            'user_name':    'suhwpark',
            'nick_name':    'nick4',    # Case: Duplicated nickName
            'picture':      'pic2'
        }
        response = self.client.post('/mypage/editor', json.dumps(data), content_type='application/json')
        print("Response : ", response)
        print("Nick After   :", User.objects.get(intra_name='suhwpark').nick_name)

    def test_duplicate_friendship(self):
        data = {
            'user_name':    'jinoh',
            'friend':       'suhwpark'
        }
        print("1st POST: ", self.client.post('/friend/add', json.dumps(data), content_type='application/json'))
        print("2nd POST: ", self.client.post('/friend/add', json.dumps(data), content_type='application/json'))
        data = {
            'user_name':    'sohyupar',
            'friend':       'suhwpark'
        }
        self.client.post('/friend/add', json.dumps(data), content_type='application/json')
        data['friend'] = 'jinoh'
        self.client.post('/friend/add', json.dumps(data), content_type='application/json')

        # 유저1의 친구목록
        friends = FriendShip.objects.filter(owner=self.user1).all()
        # 유저3을 친구로 가지는 유저목록
        friend_with_suhpark = FriendShip.objects.filter(friend=self.user3).all()

        for i in friends:
            print("user1's friend:", i.friend)

        for i in friend_with_suhpark:
            print(i.owner, "is close with user3")

#   파일분리 안하고 일단넣음
    def test_delete_friendship(self):
        data = {
            'user_name':    'jinoh',
            'friend':       'suhwpark'
        }
        print("1nd DEL: ", self.client.delete('/friend/delete', json.dumps(data), content_type='application/json'))
        print("1st ADD: ", self.client.post('/friend/add', json.dumps(data), content_type='application/json'))
        print("2nd DEL: ", self.client.delete('/friend/delete', json.dumps(data), content_type='application/json'))

        friends = FriendShip.objects.filter(owner=self.user2).all()
        for i in friends:   # 출력 안되는게 맞음
            print("user2's friend:", i.friend)
