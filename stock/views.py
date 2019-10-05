from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import StockForm, SharesForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from stock.models import Stock, Shares, Transaction_History
from trading.models import Trading_Account
from users.models import UserFund, FirstTime

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

    #Get user's trading accounts
    user= request.user
    trading_accounts = Trading_Account.objects.filter(user_id=user.id)

    #call quick buy from modal
    form = SharesForm(request.POST or None)
    if request.method == 'POST':
        stock_quick_buy(request, form)

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
    'trading_accounts': trading_accounts,
    'form': form,
    })

@login_required(login_url="/users")
def stock_quick_buy(request, form):
    if form.is_valid():
        shares = form.save(commit=False)
        stock_ticker = request.POST.get('stock_ticker')
        # Check stock exists
        try:
            stock = Stock.objects.get(stock_ticker=stock_ticker)
        except Stock.DoesNotExist:
            raise Http404
        transaction_history = Transaction_History()
        tradingID = request.POST.get('selectedAccount')

        # Check selected trading account exists for user
        if Trading_Account.objects.filter(pk=tradingID).exists():
            user= request.user
            trading_accounts = Trading_Account.objects.filter(user_id=user.id)

            # Check there are enough shares for quantity
            quantity = shares.shares_amount
            stock_available = stock.stock_max - stock.stock_sold
            if 0 < quantity <= stock_available:

                # Check user has enough funds
                if (user.userfund.fund - stock.stock_price * quantity) >= 0:
                    # Check if user already owns shares in stock
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
                        shares.user = user
                        shares.save()
                        stock.save()
                        user.userfund.save()
                        form = SharesForm()
                        try:
                            getName = Trading_Account.objects.get(pk=tradingID)
                        except Trading_Account.DoesNotExist:
                            return Http404
                        # Add to trading history
                        transaction_history.user = user
                        transaction_history.trading_name = getName.trading_name
                        transaction_history.stock_name = stock.stock_name
                        transaction_history.stock_gics = stock.stock_gics
                        transaction_history.stock_price = stock.stock_price
                        transaction_history.no_of_shares = quantity
                        transaction_history.funds = stock.stock_price * quantity
                        transaction_history.transaction = 'P'
                        transaction_history.save()
                        messages.success(request, 'Not enough shares available')
                    else:
                        messages.error(request, 'Not enough shares available')
                else:
                    messages.error(request, 'Not enough funds')
            else:
                messages.error(request, 'Quantity not in range')
        else:
            messages.error(request, 'Please create a trading account')

@login_required(login_url="/users")
def stock_buy(request, stock_ticker, *args, **kwargs):
    stock = request.GET.get('stock')
    try:
        stock = Stock.objects.get(stock_ticker=stock_ticker)
    except Stock.DoesNotExist:
        raise Http404
    stock_available = stock.stock_max - stock.stock_sold
    user= request.user
    try:
        default_trading = Trading_Account.objects.get(user_id=user.id, is_default=True)
    except Trading_Account.DoesNotExist:
        default_trading = None
    trading_accounts = Trading_Account.objects.filter(user_id=user.id)
    transaction_history = Transaction_History()
    form = SharesForm(request.POST or None)
    if request.method == 'POST':
        try:
            firstTime = FirstTime.objects.get(user=request.user.id, isFirstTime=True)
            firstTime.isFirstTime = False
            firstTime.save()
        except FirstTime.DoesNotExist:
            firstTime = None
        if form.is_valid():
            tradingID = request.POST.get('selectedAccount')
            shares = form.save(commit=False)
            quantity = shares.shares_amount
            if Trading_Account.objects.filter(pk=tradingID).exists():
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
                            shares.user = user
                            shares.save()
                            stock.save()
                            user.userfund.save()
                            form = SharesForm()
                            try:
                                getName = Trading_Account.objects.get(pk=tradingID)
                            except Trading_Account.DoesNotExist:
                                return Http404
                            # Add to trading history
                            transaction_history.user = user
                            transaction_history.trading_name = getName.trading_name
                            transaction_history.stock_name = stock.stock_name
                            transaction_history.stock_gics = stock.stock_gics
                            transaction_history.stock_price = stock.stock_price
                            transaction_history.no_of_shares = quantity
                            transaction_history.funds = stock.stock_price * quantity
                            transaction_history.transaction = 'P'
                            transaction_history.save()
                            return redirect('/stock/buy/'+stock_ticker+'?status=successful')
                        else:
                            messages.error(request, 'Not enough shares available')
                    else:
                        messages.error(request, 'Not enough funds')
                else:
                    messages.error(request, 'Quantity not in range')
            else:
                messages.error(request, 'Please create a trading account')
    status = request.GET.get('status')
    if status == 'successful':
        messages.success(request, 'Success!, you can view your transaction in transaction history.')
    data = get_historical(stock_ticker+".ax")
    context = {
        'stock_ticker': stock_ticker,
        'stock_name': stock.stock_name,
        'stock_price' : stock.stock_price,
        'stock_dayChange' : stock.stock_dayChange,
        'stock_dayChangePercent' : stock.stock_dayChangePercent,
        'stock_max': stock.stock_max,
        "stock_sold":  stock.stock_sold,
        'stock_available': stock_available,
        'trading_accounts': trading_accounts,
        'default_trading': default_trading,
        'form': form,
        'historical': data
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
                    shares.user = user
                    shares.save()
                    user.userfund.save()
                    # Add to trading history
                    transaction_history.user = user
                    transaction_history.trading_name = tradingID.trading_name
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
    'price': stock.stock_price,
    'form': form,
    }
    return render(request, 'stock/stock_sell.html', context)
