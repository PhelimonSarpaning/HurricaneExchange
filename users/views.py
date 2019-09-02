from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from .forms import UserFundForm, userEmailForm

# Create your views here.
def users_signup_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = userEmailForm(request.POST)
        fundForm = UserFundForm(request.POST)
        if form.is_valid() and fundForm.is_valid():
            user = form.save()

            fund = fundForm.save(commit=False)
            fund.user = user
            fund.save()

            login(request, user)
            return redirect('index')
    else:
        form = userEmailForm()
        fundForm = UserFundForm(initial={'fund': 1000000})
    context = {
        'form': form,
        'fundForm': fundForm,
    }
    return render(request, 'users/users_signup.html', context)

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
    context = {
        'form': form,
    }
    return render(request, 'users/users_login.html', context)

def users_logout_view(request, *args, **kwargs):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
