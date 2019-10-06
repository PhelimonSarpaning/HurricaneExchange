from django.core.management.base import BaseCommand, CommandError
from stock.models import Stock
import pyasx.data.companies

STOCKAMOUNT_DIVISOR = 10000000000

class Command(BaseCommand):
    help = "refresh stock information on the database"

    def handle(self, *args, **options):
        listedCompanies = pyasx.data.companies.pyasx.data.companies.get_listed_companies()

        for company in listedCompanies:
            try:
                 stock = Stock.objects.get(stock_name=company["name"])
            except Stock.DoesNotExist:
                Stock.objects.create(stock_name= company["name"],
                                    stock_ticker = company["ticker"],
                                    stock_gics = company["gics_industry"],
                                    stock_max = 1000)
                print('Stock "%s" does not exist, added to database' % company["ticker"])

            try:
                currStockInfo = pyasx.data.companies.get_company_info(company["ticker"])
                currStock = Stock.objects.get(stock_name=company["name"])
                print(currStockInfo["primary_share"]["last_price"])
                currStock.stock_price= float(currStockInfo["primary_share"]["last_price"])
                currStock.stock_dayChange = float(currStockInfo["primary_share"]["day_change_price"])
                currStock.stock_dayChangePercent = currStockInfo["primary_share"]["day_change_percent"]
                currStock.stock_hasValidInfo = True;
                currStock.stock_max =int( STOCKAMOUNT_DIVISOR/currStock.stock_price)
                currStock.save();
                print('Stock "%s" has valid Info, prices updated' % company["ticker"])
            except (pyasx.data.UnknownTickerException, ValueError) as e:
                currStock.stock_hasValidInfo = False;
                print('Stock "%s" does not have valid Info, ValidInfo set to False' % company["ticker"])
