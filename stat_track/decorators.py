import functools

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import League, MatchDay, Player


def get_league(*args, **kwargs):
    """
    this function extracts an instance of the League model from the kwargs passed to the decorator,
    depending on the context. If the kwargs does not pass the key "league_id", "matchday_id" ... 
    the function raises a ValueError.
    """
    
    league_id = kwargs.get('league_id')
    if league_id:
        league = get_object_or_404(League, pk=league_id)
        return league
    
    matchday_id = kwargs.get('matchday_id')
    if matchday_id:
        matchday = get_object_or_404(MatchDay, pk=matchday_id)
        league = matchday.league
        return league
    
    else:
        raise ValueError("Missing argument.")


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
        matchday_id = kwargs.get('matchday_id')
        
        league = get_league(*args, **kwargs)

        if league in player.leagues.all() or user == league.owner:
            return view_func(request, *args, **kwargs)

        messages.error(request, "You have no access to this league.")
        return redirect(redirect_url)
    return wrapper


def is_league_owner(view_func, redirect_url="home"):
    """
    this decorator checks if user is owner of league to prevent regular users access certain views and features.
    By default, if the user is not the owner he is redirected to the home view.
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user

        league = get_league(*args, **kwargs)

        if user == league.owner:
            return view_func(request, *args, **kwargs)

        messages.error(request, "You have no access to manage league.")
        return redirect(redirect_url)
    return wrapper