from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
# from .forms import UsersForm

# Create your views here.

# def users_signup_view(request, *args, **kwargs):
#     form = UsersForm(request.POST or None)
#     if (form.is_valid()):
#         form.save()
#         form = UsersForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'users/users_signup.html', context)

def users_signup_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pages:index')
            # log user in
    else:
        form = UserCreationForm()
    return render(request, 'users/users_signup.html', {'form': form})
