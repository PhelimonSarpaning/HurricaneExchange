from django.http import HttpResponse
from django.shortcuts import render
from trading.models import Trading_Account
from django.views.decorators.cache import cache_control
from users.models import FirstTime

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index_view(request, *args, **kwargs):

    return render(request, 'index.html', {})
