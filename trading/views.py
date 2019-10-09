from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TradingForm, DateForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Trading_Account
from stock.models import Shares, Stock, Transaction_History
from stock.forms import SharesForm
# Create your views here.

@login_required(login_url="/users")
def trading_list_view(request, *args, **kwargs):
    queryset = Trading_Account.objects.filter(user_id=request.user.id)
    no_trading = 'It appears you have no trading accounts. Please add a trading account'
    trading_list =[]
    try:
        currentDefault = Trading_Account.objects.get(user_id=request.user.id, is_default=True)
        defaultStockAmount = Shares.objects.filter(tradingID=currentDefault.id).count()
        defaultShares = Shares.objects.filter(tradingID=currentDefault.id)
        defaultValue = 0
        for share in defaultShares:
            defaultValue += share.shares_amount * share.stockID.stock_price
    except Trading_Account.DoesNotExist:
        currentDefault = None
        defaultStockAmount = None
        defaultShares = None
        defaultValue = None
    if queryset.exists():
        no_trading = ''

        for trading in queryset:
            trading_dict = {}
            trading_dict['id'] = trading.id
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
        'no_trading': no_trading,
        'default_trading': currentDefault,
        'defaultStockAmount': defaultStockAmount,
        'defaultValue': defaultValue
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

    trading_accounts = Trading_Account.objects.filter(~Q(id=id), user_id=request.user.id)

    if request.method == 'POST':
        try:
            currentDefault = Trading_Account.objects.get(user_id=request.user.id, is_default=True)
            currentDefault.is_default = False
            currentDefault.save()
        except Trading_Account.DoesNotExist:
            pass
        try:
            obj = Trading_Account.objects.get(id=id)
            if (obj.user_id != request.user):
                return redirect('/trading/')
            obj.is_default = True
            obj.save()
            currentDefault = obj

            objShares = Shares.objects.filter(tradingID=obj.id)
            no_Shares = 'It appears you have no Shares for this trading account. Please add Shares'
            shares_exist = False
            accounts_exist = False
            share_list =[]
            if objShares.exists():
                no_Shares = ''
                shares_exist = True
                if trading_accounts.exists():
                    accounts_exist= True

                for shares in objShares:
                    share_dict = {}
                    share_dict[shares.stockID] = shares.shares_amount * shares.stockID.stock_price
                    share_list.append(share_dict)

        except Trading_Account.DoesNotExist:
            return Http404

    else:
        try:
            obj = Trading_Account.objects.get(id=id)
            if (obj.user_id != request.user):
                return redirect('/trading/')
            objShares = Shares.objects.filter(tradingID=obj.id)
            no_Shares = 'It appears you have no Shares for this trading account. Please add Shares'
            shares_exist = False
            accounts_exist = False
            share_list =[]
            if objShares.exists():
                no_Shares = ''
                shares_exist = True
                if trading_accounts.exists():
                    accounts_exist= True

                for shares in objShares:
                    share_dict = {}
                    share_dict[shares.stockID.stock_ticker] = shares.shares_amount * shares.stockID.stock_price
                    share_list.append(share_dict)
        except Trading_Account.DoesNotExist:
            raise Http404
        try:
            currentDefault = Trading_Account.objects.get(user_id=request.user.id, is_default=True)
        except Trading_Account.DoesNotExist:
            currentDefault = None

    form = SharesForm(request.POST or None)


    #sells selected shares click and refreshes page
    if request.method == 'POST' and 'sell-submit' in request.POST:
        stock_ticker = request.POST.get('stock_ticker')
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
                        return redirect('/trading/'+str(id))
                else:
                    messages.error(request, 'You do not own that many shares ')
                form = SharesForm()
            else:
                messages.error(request, 'Quantity not in range')
        return redirect('/trading/'+str(id))

    #sells all shares on sell all button click and refreshes page
    if request.method == 'POST' and 'sell-all-button' in request.POST:
        sell_all_shares(request, objShares)
        return redirect('/trading/'+str(id))

    #transfers all current trading account shares to selected account
    if request.method == 'POST' and 'transfer-all-button' in request.POST:
        tradingID = request.POST.get('selectedAccount')
        # Check selected trading account exists for user
        tradingAccount = Trading_Account.objects.filter(pk=tradingID)
        if tradingAccount.exists():
            user= request.user
            for shares in objShares:
                shares.tradingID= tradingAccount[0]
                shares.save()
        return redirect('/trading/'+str(id))

    context = {
        'trading_account': obj,
        'share_value': share_list,
        'sharesObj': objShares,
        'no_Shares': no_Shares,
        'defaultAccount': currentDefault,
        'trading_accounts': trading_accounts,
        'shares_exist': shares_exist,
        'accounts_exist': accounts_exist,
        'form': form
    }
    return render(request, 'trading/trading_detail.html', context)

#method to sell all shares in trading account
@login_required(login_url="/users")
def sell_all_shares(request, objShares):
    for shares in objShares:
        user = request.user
        stock = shares.stockID
        user.userfund.fund -= stock.stock_price * shares.shares_amount
        stock.stock_sold -= shares.shares_amount
        stock.save()
        shares.delete()
        user.userfund.save()

@login_required(login_url="/users")
def trading_delete_view(request, id, *args, **kwargs):

    #get users other trading accounts for dropdown
    trading_accounts = Trading_Account.objects.filter(~Q(id=id), user_id=request.user.id)

    #set account action options to display if account has shares
    tradingObject = Trading_Account.objects.get(id=id)
    objShares = Shares.objects.filter(tradingID=tradingObject.id)
    shares_exist = False
    accounts_exist= False
    if objShares.exists():
        shares_exist = True
        if trading_accounts.exists():
            accounts_exist= True

    if request.method == 'POST':
        try:
            if (shares_exist and accounts_exist):
                if (request.POST['accountAction'] == 'sell'):
                    sell_all_shares(request, objShares)
                elif (request.POST['accountAction'] == 'transfer'):
                    tradingID = request.POST.get('selectedAccount')
                    # Check selected trading account exists for user
                    tradingAccount = Trading_Account.objects.filter(pk=tradingID)
                    if tradingAccount.exists():
                        user= request.user
                        for shares in objShares:
                            shares.tradingID= tradingAccount[0]
                            shares.save()
            elif (shares_exist):
                sell_all_shares(request, objShares)
            tradingObject.delete()
        except Trading_Account.DoesNotExist:
            pass
        return redirect('trading:list')
        context = {
            'trading_account': tradingObject,
            'trading_accounts': trading_accounts,
            'shares_exist': shares_exist,
            'accounts_exist': accounts_exist
        }
    else:
        try:
            tradingObject = Trading_Account.objects.get(id=id)
        except Trading_Account.DoesNotExist:
            raise Http404
        context = {
            'trading_account': tradingObject,
            'trading_accounts': trading_accounts,
            'shares_exist': shares_exist,
            'accounts_exist': accounts_exist
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
                qs = Transaction_History.objects.filter(user_id=request.user.id, date_of_transaction__date__range=[startDate, endDate]).order_by('-date_of_transaction')
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
        qs = Transaction_History.objects.filter(user_id=request.user.id).order_by('-date_of_transaction')
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
