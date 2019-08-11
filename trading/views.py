from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TradingForm

from .models import Trading_Account
from stock.models import Stock_Amount
# Create your views here.

def trading_list_view(request, *args, **kwargs):
    queryset = Trading_Account.objects.filter(user_id=request.user.id)
    no_trading = 'It appears you have no trading accounts. Please add a trading account'
    if queryset.exists():
        no_trading = ''
    context = {
        'trading_accounts': queryset,
        'no_trading': no_trading
    }
    return render(request, 'trading/trading_list.html', context)


def trading_create_view(request, *args, **kwargs):
    form = TradingForm(request.POST or None)
    if form.is_valid():
        trading = form.save(commit=False)
        trading.user_id = request.user
        trading.save()
        form = TradingForm()
        return redirect('trading:list')
    context = {
        'form': form,
    }
    return render(request, 'trading/trading_create.html', context)

def trading_detail_view(request, id, *args, **kwargs):
    try:
        obj = Trading_Account.objects.get(id=id)
        objStock = Stock_Amount.objects.filter(trading_id=obj.id)
    except Trading_Account.DoesNotExist:
        raise Http404
    context = {
        'trading_account': obj,
        'stock_amount': objStock
    }
    return render(request, 'trading/trading_detail.html', context)