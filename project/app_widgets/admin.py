from django.contrib import admin
from .models import Task, SimpleTodoList, TimeTable, Day


@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = ["title", "created_at", "completed"]


@admin.register(SimpleTodoList)
class AdminSimpleTodoList(admin.ModelAdmin):
    list_display = ["name", "title", "created_at"]


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "created_at"]
