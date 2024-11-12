from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path("add-widget/", WidgetMaker.as_view(), name="add_widget"),
    path("update-title/", update_widget_title, name="udpate_widget_title"),
]
