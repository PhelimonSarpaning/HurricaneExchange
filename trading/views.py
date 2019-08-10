from django.shortcuts import render
from .forms import TradingForm
# Create your views here.
def trading_create_view(request, *args, **kwargs):
    form = TradingForm(request.POST or None)
    if form.is_valid():
        trading = form.save(commit=False)
        trading.user_id = request.user
        trading.save()
        form = TradingForm()
    context = {
        'form': form,
    }
    return render(request, 'trading/trading_create.html', context)