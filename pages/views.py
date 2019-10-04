from django.http import HttpResponse
from django.shortcuts import render
from trading.models import Trading_Account
from django.views.decorators.cache import cache_control
from users.models import UserFund
from stock.models import Shares

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index_view(request, *args, **kwargs):
    sharesObj = None
    leaderObj = None
    if request.user.is_authenticated:
        try:
            sharesObj = Shares.objects.filter(user=request.user)
        except Shares.DoesNotExist:
            sharesObj = None
        try:
            leaderQuery = UserFund.objects.all()
            leaderObj = leaderQuery.order_by('-fund')
        except UserFund.DoesNotExist:
            leaderObj = None
    context = {
        'sharesObj': sharesObj,
        'leaderObj': leaderObj
    }
    return render(request, 'index.html', context)
