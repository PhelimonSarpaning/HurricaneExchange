from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
def users_signup_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
            
    else:
        form = UserCreationForm()
    return render(request, 'users/users_signup.html', {'form': form})

def users_login_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'users/users_login.html', {'form': form})

def users_logout_view(request, *args, **kwargs):
    if request.method == 'POST':
        logout(request)
        return redirect('index')