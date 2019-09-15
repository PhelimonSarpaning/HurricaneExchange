from trading.models import Trading_Account

def list_trading_accounts(request):
    queryset = Trading_Account.objects.filter(user_id=request.user.id)
    defaultTrading = Trading_Account.objects.get(user_id=request.user.id, is_default=True)
    context = {
        'list_accounts': queryset,
        'default_trading': defaultTrading
    }
    return context