from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path("add_simple_todo/", add_simple_todo_list, name="add_simple_todo"),
]
