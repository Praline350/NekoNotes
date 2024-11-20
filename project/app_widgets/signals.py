from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import date

from .models import TimeTable, Day, SimpleTodoList
from .models import DAYS


class TimetableSignals:
    @staticmethod
    @receiver(post_save, sender=TimeTable)
    def create_days_for_timetable(sender, instance, created, **kwargs):
        """Créer les 7 jours de la semaine de la timetable"""
        if created:  # Si le Timetable vient d'être créé
            # Créer un Day pour chaque jour de la semaine
            for day_name, day_value in DAYS:
                Day.objects.create(timetable=instance, name=day_name)


class DaySignals:
    @staticmethod
    @receiver(post_delete, sender=Day)
    def delete_tasks_with_days(sender, instance, **kwargs):
        """Supprimer les tâches associées à ce Day si elles ne sont plus utilisées par aucun autre Day"""
        for task in instance.tasks.all():
            if not task.days.exists():  # Si la tâche n'est associée à aucun autre Day
                task.delete()


class SimpleTodoListSignals:
    @staticmethod
    @receiver(post_delete, sender=SimpleTodoList)
    def delete_tasks_if_no_other_todolist(sender, instance, **kwargs):
        """Supprimer les tâches associées à cette todolist si elles ne sont plus utilisées par aucun autre todolist"""
        for task in instance.tasks.all():
            # Si la tâche n'est liée à aucun autre SimpleTodoList
            if not task.todo_lists.exists():
                task.delete()
