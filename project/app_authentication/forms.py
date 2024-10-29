from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    login_username = forms.CharField(
        label="Nom d'utilisateur ou e-mail", max_length=150
    )
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    email = forms.EmailField(label="Adresse e-mail", max_length=254)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email
