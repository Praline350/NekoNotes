from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required

from django.views.generic import View
from django.contrib import messages

from .forms import LoginForm, SignupForm


User = get_user_model()


class WelcomeView(View):
    template_name = "authentication/welcome.html"
    signup_form_class = SignupForm

    def get(self, request):
        """Handle GET requests: instantiate blank form sign up or redirect home."""

        if request.user.is_authenticated:
            return redirect("home")
        signup_form = self.signup_form_class()
        context = {"signup_form": signup_form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        """Handle POST requests: create a new account."""
        signup_form = self.signup_form_class(request.POST)
        print("Login form data:", request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Erreur lors de l'inscription")
            print(signup_form.errors)
        context = {"signup_form": signup_form}
        return render(request, self.template_name, context=context)


@login_required
def logout_user(request):
    """Log out the user and redirect to the login page."""
    logout(request)
    return redirect("welcome")
