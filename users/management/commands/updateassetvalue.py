from django.core.management.base import BaseCommand, CommandError
from users.models import UserFund, UserAssetValue
from trading.models import Trading_Account
from stock.models import Shares, Stock
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "updates all users assetsValues, should be run regularly, when stocks are updated"

    def handle(self, *args, **options):
        users = UserFund.objects.all()
        for fund in users:
            assetVal = 0
            user = fund.user_id
            tradingAccounts = Trading_Account.objects.filter(user_id=user)
            for account in tradingAccounts:
                shares = Shares.objects.filter(tradingID = account)
                for share in shares:
                    stock = share.stockID
                    assetVal+= share.shares_amount * stock.stock_price
            fund.totalAssetValue = assetVal + fund.fund
            fund.save()

            
            #create object for historivalGraph
            newUserAssetVal = UserAssetValue()
            newUserAssetVal.user_id = User.objects.get(id=user)
            newUserAssetVal.totalAssetValue = fund.totalAssetValue
            newUserAssetVal.save()
