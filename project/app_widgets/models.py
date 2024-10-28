from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from app_dashboards.models import Widget


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SimpleTodoList(Widget):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    progress_bar = models.PositiveIntegerField(
        default=100, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tasks = models.ManyToManyField(Task, related_name="todo_lists")

    def __str__(self):
        return self.name

    def update_progress_bar(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            self.progress_bar = 100
        else:
            completed_tasks = self.tasks.filter(completed=True).count()
            self.progress_bar = int((completed_tasks / total_tasks) * 100)
        self.save()
