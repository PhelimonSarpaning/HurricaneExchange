from django import forms

from .models import Users

class UsersForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={"placeholder": "Please enter your first name"}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={"placeholder": "Please enter your last name"}))
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={"placeholder": "Please enter your password"}))

    class Meta:
        model = Users
        fields = [
            'first_name',
            'last_name',
            'email',
            'password'
        ]