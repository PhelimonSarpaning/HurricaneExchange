from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserFund, FirstTime

class UserFundForm(forms.ModelForm):
    fund = forms.FloatField(widget=forms.HiddenInput(), initial=1000000)
    class Meta:
        model = UserFund
        fields = [
            'fund'

        ]


class userSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FirstTimeForm(forms.ModelForm):
    firstTime = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=True)
    class Meta:
        model = FirstTime
        fields = [
            'isFirstTime'
        ]