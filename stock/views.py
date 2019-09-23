from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import StockForm, SharesForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from stock.models import Stock, Shares, Transaction_History
from trading.models import Trading_Account
from users.models import UserFund

#for historical graph
from yahoo_historical import Fetcher
from datetime import datetime
import json
import pandas as pd
import numpy as np
# Create your views here.

@login_required(login_url="/users")
def stock_create_view(request, id, *args, **kwargs):
    form = StockForm(request.POST or None)
    if form.is_valid():
        stock = form.save(commit=False)
        stock.trading_id = Trading_Account.objects.get(id=id)
        stock.save()
        form = StockForm()
        return redirect('/trading/' + str(stock.trading_id.id))
    context = {
        'form': form,
        'trading_account': Trading_Account.objects.get(id=id)
    }
    return render(request, 'stock/stock_create.html', context)

@login_required(login_url="/users")
def stock_detail_view(request, id, *args, **kwargs):
    try:
        obj = Stock_Amount.objects.get(id=id)
    except Stock_Amount.DoesNotExist:
        raise Http404
    context = {
        'stock_amount': obj,
    }
    return render(request, 'stock/stock_detail.html', context)

@login_required(login_url="/users")
def stock_list_view(request, *args, **kwargs):
    stock_list = Stock.objects.all().filter(stock_hasValidInfo=True).order_by('-stock_price')
    paginator = Paginator(stock_list, 10)
    page = request.GET.get('page')
    try:

        if(int(page) < 0):
            page=1
        if(int(page)>paginator.num_pages):
            page=paginator.num_pages
        stocks = paginator.get_page(page)
    except:
        stocks = paginator.get_page(page)

    #index of the current page
    index = stocks.number - 1
    #maximum index of pages
    max_index = len(paginator.page_range)
    #set range of index to 7
    start_index = index - 3 if index > 3 else 0
    #end_index = index + 3 if index <= max_index - 3 else max_index
    if index <= max_index:
        if index <= 3:
            end_index = 7
        else:
            end_index = index+4
    else:
        end_index = max_index
    page_range = list(paginator.page_range)[start_index:end_index]
    return render(request, 'stock/stock_list.html', {
    'stocks': stocks,
    'page_range':page_range,
    })

@login_required(login_url="/users")
def stock_buy(request, stock_ticker, *args, **kwargs):
    stock = request.GET.get('stock')
    try:
        stock = Stock.objects.get(stock_ticker=stock_ticker)
    except Stock.DoesNotExist:
        raise Http404
    stock_available = stock.stock_max - stock.stock_sold
    user= request.user
    data = get_historical(stock_ticker+".ax")
    trading_accounts = Trading_Account.objects.filter(user_id=user.id)
    transaction_history = Transaction_History()
    form = SharesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            tradingID = request.POST.get('selectedAccount')
            shares = form.save(commit=False)
            quantity = shares.shares_amount
            if 0 < quantity <= stock_available:
                if (user.userfund.fund - stock.stock_price * quantity) >= 0:
                    if stock_available - quantity >= 0:
                        if Shares.objects.filter(tradingID=tradingID, stockID=stock).exists():
                            shares = Shares.objects.get(tradingID=tradingID, stockID=stock)
                            shares.shares_amount += quantity
                        else:
                            tradingAccount = Trading_Account.objects.filter(pk=tradingID)
                            shares.tradingID= tradingAccount[0]
                            shares.stockID = stock
                        stock.stock_sold += quantity
                        user.userfund.fund-= stock.stock_price * quantity
                        shares.save()
                        stock.save()
                        user.userfund.save()
                        form = SharesForm()

                        # Add to trading history
                        transaction_history.user = user
                        transaction_history.stock_name = stock.stock_name
                        transaction_history.stock_gics = stock.stock_gics
                        transaction_history.stock_price = stock.stock_price
                        transaction_history.no_of_shares = quantity
                        transaction_history.funds = stock.stock_price * quantity
                        transaction_history.transaction = 'P'
                        transaction_history.save()

                        return redirect('/stock/buy/'+stock_ticker)
                    else:
                        messages.error(request, 'Not enough shares available')
                else:
                    messages.error(request, 'Not enough funds')
            else:
                messages.error(request, 'Quantity not in range')

    context = {
        'stock_ticker': stock_ticker,
        'stock_name': stock.stock_name,
        'stock_price' : stock.stock_price,
        'stock_available': stock_available,
        'trading_accounts': trading_accounts,
        'form': form,
        'historical':data,
    }
    return render(request, 'stock/stock_buy.html', context)

def get_historical(stock_ticker):
    data = Fetcher(stock_ticker, [1990,1,1]).getHistorical()
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.drop(columns=['Open', 'High', 'Low', 'Adj Close', 'Volume'])
    data['Date']= pd.to_datetime(data['Date']).values.astype(np.int64) // 10**6
    data = data.rename(columns={"Date": "x", "Close": "y"})
    data = data.dropna()
    data = data.to_dict('records')
    return data

@login_required(login_url="/users")
def stock_sell(request, id, stock_ticker, *args, **kwargs):
    try:
        stock = Stock.objects.get(stock_ticker=stock_ticker)
    except Stock.DoesNotExist:
        raise Http404

    tradingID  = Trading_Account.objects.get(id=id)
    transaction_history = Transaction_History()
    try:
        shares = Shares.objects.get(tradingID=tradingID, stockID=stock)
    except Shares.DoesNotExist:
        raise Http404

    user= request.user

    form = SharesForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            quantity = form.cleaned_data['shares_amount']
            if 0 < quantity <= shares.shares_amount:
                if (shares.shares_amount - quantity) >= 0:
                    stock.stock_sold -= quantity
                    shares.shares_amount -= quantity
                    user.userfund.fund += stock.stock_price * quantity
                    stock.save()
                    shares.save()
                    user.userfund.save()

                    # Add to trading history
                    transaction_history.user = user
                    transaction_history.stock_name = stock.stock_name
                    transaction_history.stock_gics = stock.stock_gics
                    transaction_history.stock_price = stock.stock_price
                    transaction_history.no_of_shares = quantity
                    transaction_history.funds = stock.stock_price * quantity
                    transaction_history.transaction = 'S'
                    transaction_history.save()

                    if shares.shares_amount == 0:
                        shares.delete()
                        return redirect('/trading/')
                else:
                    messages.error(request, 'You do not own that many shares ')
                form = SharesForm()
            else:
                messages.error(request, 'Quantity not in range')
    context = {
    'stock_name': stock.stock_name,
    'num_shares': shares.shares_amount,
    'form': form,
    }
    return render(request, 'stock/stock_sell.html', context)
