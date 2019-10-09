from trading.models import Trading_Account

from users.models import FirstTime

def list_trading_accounts(request):
    try:
        queryset = Trading_Account.objects.filter(user_id=request.user.id)
    except Trading_Account.DoesNotExist:
        queryset = None
    try:
        defaultTrading = Trading_Account.objects.get(user_id=request.user.id, is_default=True)
    except Trading_Account.DoesNotExist:
        defaultTrading = None
    try:
        firstTime = FirstTime.objects.filter(user=request.user.id, isFirstTime=True)
    except FirstTime.DoesNotExist:
        firstTime = False
    if firstTime.exists():
        firstTime = True
    context = {
        'firstTime': firstTime
    }
    context = {
        'list_accounts': queryset,
        'default_trading': defaultTrading,
        'firstTime': firstTime
    }
    return context