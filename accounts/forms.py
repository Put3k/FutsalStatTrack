from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=32, required=True, widget= forms.TextInput
                           (attrs={'placeholder':'e.g. Zinedine'}))
    last_name = forms.CharField(max_length=64, required=True, widget= forms.TextInput
                           (attrs={'placeholder':'e.g. Zidane'}))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username"
        )