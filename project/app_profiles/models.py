import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class Color(models.Model):
    name = models.CharField(max_length=48)
    hex_code = models.CharField(max_length=7)  # exemple: '#FFFFFF'

    def __str__(self):
        return f"{self.name} ({self.hex_code})"

    def clean(self):
        super().clean()
        if not re.match(r"^#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})$", self.hex_code):
            raise ValidationError(f"{self.hex_code} is not a valid hex color code.")


class Theme(models.Model):
    name = models.CharField(max_length=120)
    colors = models.ManyToManyField(Color, related_name="themes")

    def __str__(self):
        return self.name


class Palette(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    primary = models.ForeignKey(
        Color,
        related_name="primary_palette",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    secondary = models.ForeignKey(
        Color,
        related_name="secondary_palette",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    third = models.ForeignKey(
        Color,
        related_name="third_palette",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Palette {self.name}"


class UiSetting(models.Model):
    background_color = models.ForeignKey(
        Color, on_delete=models.SET_NULL, null=True, blank=True
    )
    text_color = models.ForeignKey(
        Color,
        related_name="profile_text_color",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    palette = models.ForeignKey(
        Palette,
        related_name="profile_palette",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.profile:  # self.profile est une instance de Profile
            return f"{self.profile.user.username}'s UI Settings"
        return "UI Settings"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatar_profiles", blank=True, null=True)
    ui_settings = models.OneToOneField(
        UiSetting,
        on_delete=models.SET_NULL,
        related_name="profile",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
