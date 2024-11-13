from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path("add-widget/", WidgetMaker.as_view(), name="add_widget"),
    path("delete-widget/", delete_widget, name="delete_widget"),
    # TodoList
    path("update-title/", update_widget_title, name="udpate_widget_title"),
    # Task
    path("add-task/", add_task, name="add_task"),
    path("task/delete/", delete_task, name="delete_task"),
    path("task/update-title/", update_task_title, name="update_task_title"),
    path("task/update-status/", update_task_status, name="update_task_status"),
]
