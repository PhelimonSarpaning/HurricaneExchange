from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/users/')
def dashboard(request):
	template = loader.get_template('dashboard/index.html')
	username = request.user.get_username()
	context = {
		'username': username
	}
	return render(request,'dashboard/index.html', context)
