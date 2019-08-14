from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserFund

class UserFundForm(forms.ModelForm):
    class Meta:
        model = UserFund
        fields = [
            'fund'
        ]
