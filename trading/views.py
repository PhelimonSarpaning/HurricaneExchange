from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TradingForm
from django.contrib.auth.decorators import login_required

from .models import Trading_Account
from stock.models import Stock_Amount
# Create your views here.

@login_required(login_url="/users")
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

@login_required(login_url="/users")
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

@login_required(login_url="/users")
def trading_detail_view(request, id, *args, **kwargs):
    try:
        obj = Trading_Account.objects.get(id=id)
        objStock = Stock_Amount.objects.filter(trading_id=obj.id)
        no_stock = 'It appears you have no stock for this trading account. Please add stock'
        if objStock.exists():
            no_stock = ''
    except Trading_Account.DoesNotExist:
        raise Http404
    context = {
        'trading_account': obj,
        'stock_amount': objStock,
        'no_stock': no_stock
    }
    return render(request, 'trading/trading_detail.html', context)