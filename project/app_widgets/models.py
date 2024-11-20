from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from datetime import datetime, timedelta, date

from app_dashboards.models import Widget, Dashboard

# Constantes :

DAYS = [
    ("Monday", "monday"),
    ("Tuesday", "tuesday"),
    ("Wednesday", "wednesday"),
    ("Thursday", "thursday"),
    ("Friday", "friday"),
    ("Saturday", "saturday"),
    ("Sunday", "sunday"),
]


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    recurring = models.BooleanField(default=False)
    start_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)
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
    progress_bar = models.PositiveIntegerField(
        default=100, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tasks = models.ManyToManyField(Task, related_name="todo_lists", blank=True)

    def __str__(self):
        return self.name


class TimeTable(Widget):
    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, related_name="time_table"
    )
    name = models.CharField(max_length=120, default="Time Table")
    title = models.CharField(max_length=120, default="Time Table")
    week_number = models.PositiveIntegerField(null=True)
    period = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculer la période de la semaine à partir de la date actuelle
        start_date = self.get_start_of_week()
        end_date = start_date + timedelta(
            days=6
        )  # Fin de la semaine, 6 jours après le début
        self.period = f"from {start_date.day} to {end_date.day}"
        super(TimeTable, self).save(*args, **kwargs)

    def get_start_of_week(self):
        """Retourne le début de la semaine (lundi de la semaine courante)."""
        today = datetime.today()
        start_of_week = today - timedelta(
            days=today.weekday()
        )  # Lundi de cette semaine
        return start_of_week

    @property
    def current_week_number(self):
        return date.today().isocalendar().week


class Day(models.Model):
    timetable = models.ForeignKey(
        TimeTable, on_delete=models.CASCADE, related_name="days"
    )
    name = models.CharField(max_length=20, choices=DAYS)
    tasks = models.ManyToManyField(Task, related_name="days", blank=True)
