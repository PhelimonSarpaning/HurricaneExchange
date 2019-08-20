from django.test import TestCase
from trading.models import Trading_Account
from users.models import User

# Create your tests here.
class TradingAccountTest(TestCase):
    def setUp(self):
        user = User(username='testCase', password='testCase')
        user.save()
        user = User.objects.get(username='testCase')
        print(user)
        Trading_Account.objects.create(user_id=user, trading_name='unittestTrade')
    
    def test_tradeaccount_exists(self):
        unittesttrade = Trading_Account.objects.get(id=1)
        unittesttrade = unittesttrade.trading_name
        self.assertEqual(unittesttrade, 'unittestTrade')