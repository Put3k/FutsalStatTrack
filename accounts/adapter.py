from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url
from django.conf import settings


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if next:
            url = next
        else:
            url = settings.LOGIN_REDIRECT_URL
        return resolve_url(url)
