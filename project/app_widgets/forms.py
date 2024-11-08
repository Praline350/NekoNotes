from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()


class SimpleTodoForm(forms.Form):
    name = forms.CharField(
        label="Nom d'utilisateur",
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": "Username ...", "class": "form--field"}
        ),
    )

    class Meta:
        model = SimpleTodoList
        fields = [
            "name",
        ]
