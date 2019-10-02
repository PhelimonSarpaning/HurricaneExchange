from trading.models import Trading_Account
from stock.models import Shares
from users.models import UserFund

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
        sharesObj = Shares.objects.all()
    except Shares.DoesNotExist:
        sharesObj = None
    try:
        leaderQuery = UserFund.objects.all()
        leaderObj = leaderQuery.order_by('-fund')
    except UserFund.DoesNotExist:
        leaderObj = None
    context = {
        'list_accounts': queryset,
        'default_trading': defaultTrading,
        'sharesObj': sharesObj,
        'leaderObj': leaderObj
    }
    return context