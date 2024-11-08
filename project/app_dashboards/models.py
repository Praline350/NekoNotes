from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.auth import get_user_model

from app_profiles.models import Color, Palette


User = get_user_model()


class Dashboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dashboards")

    # theme = models.CharField(max_length=128, blank=True, null=True) # Theme deja prè établi
    # TODO : Ajouté plutot une relation a une table theme

    def __str__(self):
        return f"{self.user.username}'s Dashboard"


class Widget(models.Model):
    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, related_name="widgets"
    )
    name = models.CharField(max_length=128, default="Widget")
    description = models.TextField(blank=True, null=True)

    # Champs pour les informations Back-end

    status = models.BooleanField(default=True)
    refresh_interval = models.PositiveIntegerField(
        default=60
    )  # Interval de raffraichissement du widget (en seconde)

    # Champs pour le Front-end

    position = models.CharField(
        max_length=40, blank=True, null=True
    )  # ID de la cellule de la grille du dashboard

    resizable = models.BooleanField(default=True)

    # Dictionnaire des données pour le front (ex:  'color' :'red')
    front_data = models.JSONField(null=True, blank=True)

    class Meta:
        abstract = True  # Abstraite pour héritage

    def __str__(self):
        return self.name
