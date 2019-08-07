from django.shortcuts import render

# Create your views here.

def users_signup_view(request, *args, **kwargs):
    return render(request, 'users/users_signup.html', {})