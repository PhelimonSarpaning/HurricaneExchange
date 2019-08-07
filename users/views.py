from django.shortcuts import render
from .forms import UsersForm

# Create your views here.

def users_signup_view(request, *args, **kwargs):
    form = UsersForm(request.POST or None)
    if (form.is_valid()):
        form.save()
        form = UsersForm()
    context = {
        'form': form
    }
    return render(request, 'users/users_signup.html', context)