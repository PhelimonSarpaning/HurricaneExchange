from django.test import TestCase
from trading.models import Trading_Account
from users.models import User

# Create your tests here.
class TradingAccountTest(TestCase):
    user = User(username='testCase', password='testCase')

    def setUp(self):
        self.user.save()
        self.user = User.objects.get(username='testCase')
        print(self.user)
        Trading_Account.objects.create(user_id=self.user, trading_name='unittestTrade')

    def test_tradeaccount_exists(self):
        unittesttrade = Trading_Account.objects.get(user_id=self.user)
        unittesttrade = unittesttrade.trading_name
        self.assertEqual(unittesttrade, 'unittestTrade')
