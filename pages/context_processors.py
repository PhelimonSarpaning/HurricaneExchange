from trading.models import Trading_Account

def list_trading_accounts(request):
    queryset = Trading_Account.objects.filter(user_id=request.user.id)
    context = {
        'list_accounts': queryset,
    }
    return context