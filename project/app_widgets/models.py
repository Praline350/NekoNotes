from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from app_dashboards.models import Widget, Dashboard


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SimpleTodoList(Widget):
    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, related_name="simple_todo_list"
    )
    name = models.CharField(max_length=120, default="Simple Todo List")
    title = models.CharField(max_length=120, default="Simple Todo List")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    progress_bar = models.PositiveIntegerField(
        default=100, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tasks = models.ManyToManyField(Task, related_name="todo_lists", blank=True)

    def __str__(self):
        return self.name
