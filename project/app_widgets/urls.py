from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path("add_widget/", WidgetMaker.as_view(), name="add_widget"),
]
