from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required(login_url="/users")
def leaderboard_view(request, *args, **kwargs):
    return render(request, 'leaderboard_view.html', {})
    