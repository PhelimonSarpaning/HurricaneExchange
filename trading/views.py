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
            if objShares.exists():
                no_Shares = ''
        except Trading_Account.DoesNotExist:
            return Http404
    else:
        try:
            obj = Trading_Account.objects.get(id=id)
            objShares = Shares.objects.filter(tradingID=obj.id)
            no_Shares = 'It appears you have no Shares for this trading account. Please add Shares'
            if objShares.exists():
                no_Shares = ''
        except Trading_Account.DoesNotExist:
            raise Http404
    context = {
        'trading_account': obj,
        'Shares': objShares,
        'no_Shares': no_Shares
    }
    return render(request, 'trading/trading_detail.html', context)

@login_required(login_url="/users")
def trading_delete_view(request, id, *args, **kwargs):
    if request.method == 'POST':
        try:
            tradingObject = Trading_Account.objects.get(id=id)
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
