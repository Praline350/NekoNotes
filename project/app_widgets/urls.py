from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    # Widgets
    path("widget-manager/", WidgetMaker.as_view(), name="widget_manager"),
    # Simple todo list
    path("simple-todo/", SimpleTodoWidget.as_view(), name="simple_todo_manager"),
    # Task
    path("task/", TaskView.as_view(), name="task"),
]
