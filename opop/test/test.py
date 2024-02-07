from django.test import TestCase
from opop.models.models import User, BlockRelation

class UserBlockRelationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            intra_name='sohyupar',
            picture='testtestpic',
            total_win=0,
            total_lose=0,
            email='test@ettt.com',
        )

        self.user2 = User.objects.create(
            intra_name='parksooo',
            picture='testtestpic',
            total_win=0,
            total_lose=0,
            email='test@ettt.com',
        )

    def test_block_relation(self):
        # user1이 user2를 차단
        block_relation = BlockRelation.objects.create(blocked=self.user2, blocked_by=self.user1)

        # block_relation 인스턴스가 user2를 참조중인지 검수 -> user2가 차단당한 상태를 알고잇는지
        self.assertEquals(block_relation.blocked, self.user2)

        # user1이 차단의 주체인가?
        self.assertEquals(block_relation.blocked_by, self.user1)

        # user1이 차단한 모든 유저 조회
        blocked_users = User.objects.filter(blocked_by_relations__blocked_by=self.user1)
        print(blocked_users)
        # 이 차단한 모든 유저중에 user2가 있나여?
        self.assertTrue(self.user2 in blocked_users)

        # user2를 차단한 모든 유저 조회
        blocking_users = User.objects.filter(blocking_relations__blocked=self.user2)
        self.assertTrue(self.user1 in blocking_users)