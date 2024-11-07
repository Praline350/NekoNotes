from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path("", WelcomeView.as_view(), name="welcome"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
]
