from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from leaderboard.models import Leaderboard
from users.models import UserFund

@login_required(login_url="/users")
def leaderboard_view(request, *args, **kwargs):
    fundlist = UserFund.objects
    if (fundlist.exists()):
        context = {
            'object': fundlist,
            'noFundlist': False
        }
    else:
        context = {
            'noFundlist': True
        }
    return render(request, 'leaderboard_view.html', context)
    