from django.http import HttpResponse
from django.shortcuts import render
from trading.models import Trading_Account
from django.views.decorators.cache import cache_control
import pandas as pd
import numpy as np
from users.models import UserFund, UserAssetValue
from stock.models import Shares, Stock

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index_view(request, *args, **kwargs):
    sharesObj = None
    leaderObj = None
    data= None
    topShares = None
    if request.user.is_authenticated:
        try:
            tradingAccs = Trading_Account.objects.filter(user_id= request.user)
            sharesObj = Shares.objects.filter(tradingID__in = tradingAccs)
        except Shares.DoesNotExist:
            sharesObj = None
        try:
            leaderQuery = UserFund.objects.all()
            leaderObj = leaderQuery.order_by('-totalAssetValue')[:5]
        except UserFund.DoesNotExist:
            leaderObj = None

        try:
            topShares = Stock.objects.all()
            topShares = topShares.order_by('-stock_rating')[:5]
        except Stock.DoesNotExist:
            topShares = None
        try:
            data = get_user_historical(request.user)
        except KeyError:
            data=[]
    context = {
        'sharesObj': sharesObj,
        'leaderObj': leaderObj,
        'topShares': topShares,
        'userHistorical': data,
    }
    return render(request, 'index.html', context)

def get_user_historical(user):
    data = pd.DataFrame(list(UserAssetValue.objects.filter(user_id=user).values('date_tracked','totalAssetValue')))
    data['date_tracked']= pd.to_datetime(data['date_tracked']).values.astype(np.int64) // 10**6
    data = data.rename(columns={"date_tracked": "x", "totalAssetValue": "y"})
    data = data.dropna()
    data = data.to_dict('records')
    return data
