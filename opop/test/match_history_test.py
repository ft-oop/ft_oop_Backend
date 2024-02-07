from datetime import datetime

from django.test import TestCase
from opop.models.models import User, MatchHistory


class TestMatchHistory(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            intra_name='suhwpark',
            picture='aaaaaa',
            email='popomarin28@gmail.com',
            total_win=2,
            total_lose=0,
        )

        self.matchHistory1 = MatchHistory.objects.create(
            user=self.test_user,
            opponent_name='yongmipa',
            result='victory',
            game_type='single',
            match_date=datetime.date(datetime.now())
        )

        self.matchHistory2 = MatchHistory.objects.create(
            user=self.test_user,
            opponent_name='jino',
            result='lose',
            game_type='tournament',
            match_date=datetime.date(datetime.now())
        )

    def test_match_history(self):
        match_history = self.test_user.match_history.all()

        # 히스토리가 2개인지
        self.assertEqual(len(match_history), 2)

        # 히스토리 내용이 잘 들어가 있는지
        self.assertEqual(match_history[0].user, self.test_user)
        self.assertEqual(match_history[0].opponent_name, 'yongmipa')
        self.assertEqual(match_history[0].result, 'victory')
        self.assertEqual(match_history[0].game_type, 'single')
        self.assertEqual(match_history[0].match_date, self.matchHistory1.match_date)

        self.assertEqual(match_history[1].user, self.test_user)
        self.assertEqual(match_history[1].opponent_name, 'jino')
        self.assertEqual(match_history[1].result, 'lose')
        self.assertEqual(match_history[1].game_type, 'tournament')
        self.assertEqual(match_history[1].match_date, self.matchHistory2.match_date)
