from django import forms
from django.forms import CheckboxInput, ModelForm, TextInput

from .models import League, Match, MatchDay, MatchDayTicket, Player, Stat


class DateInput(forms.DateInput):
    input_type = "date"

class LeagueForm(forms.ModelForm):
    add_owner = forms.BooleanField(label="Include Owner in League")
    class Meta:
        model = League
        fields = [
            "name",
            "start_date"
            ]

        widgets = {
            "name": TextInput(attrs={
                "class": "form-control mb-3",
                "name": "League name",
                "placeholder": "Champions League",
                "required": "True"
            }),
            "start_date": DateInput(attrs={
                "class": "form-control w-25 mb-3",
            }),
            "add_owner": CheckboxInput(attrs={
                'class':"form-check-input",
                'type':"checkbox",
                'value':"",
                'id':"flexCheckDefault",
            })}
    

class MatchDayForm(forms.ModelForm):
    class Meta:
        model = MatchDay
        fields = ["date"]
        widgets = {
            "date": DateInput()
        }

class MatchCreator(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["team_home", "team_away", "home_goals", "away_goals"]

        widgets = {
            "team_home": forms.Select(attrs={"class":"form-control bg-dark text-white w-75"}),
            "team_away": forms.Select(attrs={"class":"form-control bg-dark text-white w-75"}),
            "home_goals": forms.NumberInput(attrs={"class":"form-control bg-dark text-white w-25"}),
            "away_goals": forms.NumberInput(attrs={"class":"form-control bg-dark text-white w-25"})
        }

class StatForm(forms.ModelForm):
    class Meta:
        model = Stat
        fields = "__all__"

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["first_name", "last_name"]

        widgets = {
            "first_name": TextInput(attrs={
                "class": "form-control mb-3",
            }),
            "last_name": TextInput(attrs={
                "class": "form-control mb-3",
            })
        }