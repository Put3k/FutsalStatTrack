import functools

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import League, Player


def is_league_member_or_owner(view_func, redirect_url="home"):
    """
    this decorator checks user permissions to access leagues to prevent unauthorized users
    from accessing views they shouldn't have access to. By default if user is not member or owner he is redirected to home view.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        player = Player.objects.get(user=user)
        league_id = kwargs.get('league_id')
        league = get_object_or_404(League, pk=league_id)

        if league in player.leagues.all() or user == league.owner:
            return view_func(request, *args, **kwargs)

        messages.error(request, "You have no access to this league.")
        return redirect(redirect_url)
    return wrapper
