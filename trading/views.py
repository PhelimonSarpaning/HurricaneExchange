from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TradingForm, DateForm
from django.contrib.auth.decorators import login_required

from .models import Trading_Account
from stock.models import Shares, Transaction_History
# Create your views here.

@login_required(login_url="/users")
def trading_list_view(request, *args, **kwargs):
    queryset = Trading_Account.objects.filter(user_id=request.user.id)
    no_trading = 'It appears you have no trading accounts. Please add a trading account'
    trading_list =[]
    if queryset.exists():
        no_trading = ''

        for trading in queryset:
            trading_dict = {}
            trading_dict['trading_account'] = trading
            trading_dict['stock_amount'] = Shares.objects.filter(tradingID=trading.id).count()
            shares = Shares.objects.filter(tradingID=trading.id)
            value = 0
            for share in shares:
                value += share.shares_amount * share.stockID.stock_price
            trading_dict['value'] = value
            trading_list.append(trading_dict)
    context = {
        'trading_accounts': trading_list,
        'no_trading': no_trading
    }
    return render(request, 'trading/trading_list.html', context)

@login_required(login_url="/users")
def trading_create_view(request, *args, **kwargs):
    form = TradingForm(request.POST or None)
    try:
        queryset = Trading_Account.objects.filter(user_id=request.user.id, is_default=True)
    except Trading_Account.DoesNotExist:
        queryset = None
    if form.is_valid():
        trading = form.save(commit=False)
        trading.user_id = request.user
        if queryset.exists():
            trading.is_default = False
        else:
            trading.is_default = True
        trading.save()
        form = TradingForm()
        return redirect('trading:list')
    context = {
        'form': form,
    }
    return render(request, 'trading/trading_create.html', context)

@login_required(login_url="/users")
def trading_detail_view(request, id, *args, **kwargs):
    if request.method == 'POST':
        try:
            currentDefault = Trading_Account.objects.get(user_id=request.user.id, is_default=True)
            currentDefault.is_default = False
            currentDefault.save()
        except Trading_Account.DoesNotExist:
            pass
        try:
            obj = Trading_Account.objects.get(id=id)
            obj.is_default = True
            obj.save()

            objShares = Shares.objects.filter(tradingID=obj.id)
            no_Shares = 'It appears you have no Shares for this trading account. Please add Shares'
            share_list =[]
            if objShares.exists():
                no_Shares = ''

                share_list =[]
                for shares in objShares:
                    share_dict = {}
                    share_dict[shares.stockID] = shares.shares_amount * shares.stockID.stock_price
                    share_list.append(share_dict)

        except Trading_Account.DoesNotExist:
            return Http404
    else:
        try:
            obj = Trading_Account.objects.get(id=id)
            objShares = Shares.objects.filter(tradingID=obj.id)
            no_Shares = 'It appears you have no Shares for this trading account. Please add Shares'
            share_list =[]
            if objShares.exists():
                no_Shares = ''

                for shares in objShares:
                    share_dict = {}
                    share_dict[shares.stockID.stock_ticker] = shares.shares_amount * shares.stockID.stock_price
                    share_list.append(share_dict)
        except Trading_Account.DoesNotExist:
            raise Http404
    context = {
        'trading_account': obj,
        'share_value': share_list,
        'sharesObj': objShares,
        'no_Shares': no_Shares
    }
    return render(request, 'trading/trading_detail.html', context)

@login_required(login_url="/users")
def trading_delete_view(request, id, *args, **kwargs):
    if request.method == 'POST':
        try:
            tradingObject = Trading_Account.objects.get(id=id)
            shares = Shares.objects.filter(tradingID=tradingObject.id)
            for share in shares:
                stock = share.stockID
                stock.stock_sold -= share.shares_amount
                stock.save()
                share.delete()
            tradingObject.delete()
        except Trading_Account.DoesNotExist:
            pass
        return redirect('trading:list')
        context = {
            'trading_account': tradingObject
        }
    else:
        try:
            tradingObject = Trading_Account.objects.get(id=id)
        except Trading_Account.DoesNotExist:
            raise Http404
        context = {
            'trading_account': tradingObject
        }
    return render(request, 'trading/trading_delete.html', context)

@login_required(login_url="/users")
def trading_history_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            startDate = form.cleaned_data['date']
            endDate = form.cleaned_data['date2']
            try:
                qs = Transaction_History.objects.filter(user_id=request.user.id, date_of_transaction__date__range=[startDate, endDate])
            except Transaction_History.DoesNotExist:
                pass
        else:
            return redirect('/trading/history')
        context = {
            'object': qs,
            'form': form,
            'startDate': str(startDate),
            'endDate': str(endDate)
        }
    else:
        qs = Transaction_History.objects.filter(user_id=request.user.id)
        form = DateForm()
        if (qs.exists()):
            context = {
                'object': qs,
                'noHistory': False,
                'form': form
            }
        else:
            context = {
                'noHistory': True
            }
    return render(request, 'trading/trading_history.html', context)
