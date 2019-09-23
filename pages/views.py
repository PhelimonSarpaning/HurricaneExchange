from django.http import HttpResponse
from django.shortcuts import render
from trading.models import Trading_Account
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index_view(request, *args, **kwargs):
    queryset = Trading_Account.objects.filter(user_id=request.user.id)
    # no_trading = 'It appears you have no trading accounts. Please add a trading account'
    firstTime = True
    if queryset.exists():
        firstTime = False
    context = {
        'firstTime': firstTime
    }
    return render(request, 'index.html', context)
