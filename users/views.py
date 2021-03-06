from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.views.decorators.cache import cache_control
from .models import UserAssetValue
import datetime


from .forms import UserFundForm, userSignupForm, FirstTimeForm


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users_signup_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = userSignupForm(request.POST)
            fundForm = UserFundForm(request.POST)
            firstTimeForm = FirstTimeForm(request.POST)
            if form.is_valid() and fundForm.is_valid() and firstTimeForm.is_valid():
                user = form.save()

                fund = fundForm.save(commit=False)
                fund.user = user
                fund.save()

                firstTime = firstTimeForm.save(commit=False)
                firstTime.user = user
                firstTime.isFirstTime = True
                firstTime.save()

                assetVal = UserAssetValue()
                assetVal.user_id = user
                assetVal.totalAssetValue = fund.fund
                assetVal.save()

                login(request, user)
                return redirect('index')
        else:
            form = userSignupForm()
            fundForm = UserFundForm(initial={'fund': 1000000})
            firstTimeForm = FirstTimeForm(initial={'isFirstTime': True})
        context = {
            'form': form,
            'fundForm': fundForm,
            'firstTimeForm': firstTimeForm
        }
        return render(request, 'users/users_signup.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users_login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('index')
    else:
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

@cache_control(no_cache=True, must_revalidate=True)
def users_logout_view(request, *args, **kwargs):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

@login_required(login_url="/users")
def users_manage_view(request, *args, **kwargs):
    return render(request, 'users/users_manage.html')
