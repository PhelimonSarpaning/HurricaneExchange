from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TradingForm

from .models import Trading_Account
# Create your views here.

def trading_list_view(request, *args, **kwargs):
    queryset = Trading_Account.objects.filter(user_id=request.user.id)
    context = {
        'trading_accounts': queryset
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

