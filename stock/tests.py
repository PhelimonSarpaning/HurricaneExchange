from django.test import TestCase
from trading.models import Trading_Account
from users.models import User, UserFund
from stock.models import Stock, Shares
class YourTestClass(TestCase):
    def setUp(self):
        self.stock = Stock(stock_name = 'testStock', stock_price =2, stock_sold = 0)
        self.stock.save()
        self.shareQuantity = 5

        self.user = User(username='testUser', password='testPw')
        self.user.save()
        self.user = User.objects.get(username='testUser')
        self.userund = UserFund(user = self.user, fund = 1000)

        Trading_Account.objects.create(user_id=self.user, trading_name='testTrade')
        self.trading =  Trading_Account.objects.get(user_id=self.user)

    def testBuyShareOnFunds(self):
        self.user.userfund.fund -= self.stock.stock_price * self.shareQuantity
        self.assertTrue(self.user.userfund.fund, 10)

    def testBuySharesOnSharesAmount(self):
        shares = Shares(shares_amount = 10)
        self.stock.stock_sold -= self.shareQuantity
        self.assertTrue(self.stock.stock_sold, 5)

    def testSellSharesOnStockSold(self):
        self.stock.stock_sold += self.shareQuantity
        self.assertTrue(self.stock.stock_sold, 5)

    def testSellSharesOnSharesAmount(self):
        shares = Shares(shares_amount = self.shareQuantity)
        self.stock.stock_sold += shares.shares_amount
        self.assertTrue(self.stock.stock_sold, 5)
