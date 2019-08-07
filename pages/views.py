from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        username = request.user.get_username()
        context = {
            'username': username
        }
    else:
        context = {
            'username': 'Guest'
        }
        
    return render(request, 'index.html', context)
