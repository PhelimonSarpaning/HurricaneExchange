from django.core.management.base import BaseCommand, CommandError
from stock.models import Stock
import pyasx.data.companies

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
                print('Stock "%s" does not exist, added to database' % company["name"])
