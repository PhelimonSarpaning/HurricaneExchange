from trading.models import Trading_Account

def list_trading_accounts(request):
    try:
        queryset = Trading_Account.objects.filter(user_id=request.user.id)
    except Trading_Account.DoesNotExist:
        queryset = None
    try:
        defaultTrading = Trading_Account.objects.get(user_id=request.user.id, is_default=True)
    except Trading_Account.DoesNotExist:
        defaultTrading = None
    context = {
        'list_accounts': queryset,
        'default_trading': defaultTrading
    }
    return context