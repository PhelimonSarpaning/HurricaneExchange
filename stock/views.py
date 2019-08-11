from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import StockForm

from stock.models import Stock_Amount
from trading.models import Trading_Account
# Create your views here.

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
    }
    return render(request, 'stock/stock_create.html', context)