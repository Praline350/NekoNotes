import pytest
from django.contrib.auth import get_user_model
from app_profiles.models import Color, Palette, Profile, UiSetting

User = get_user_model()


@pytest.mark.django_db  # Cette annotation permet d'accéder à la base de données
class TestColor:
    def test_color_creation(self):
        color = Color.objects.create(name="Red", hex_code="#FF0000")

        assert color.name == "Red"
        assert color.hex_code == "#FF0000"
        assert str(color) == "Red (#FF0000)"


@pytest.mark.django_db
class TestPalette:
    def test_palette_creation(self):
        primary_color = Color.objects.create(name="Blue", hex_code="#0000FF")
        secondary_color = Color.objects.create(name="Green", hex_code="#00FF00")
        third_color = Color.objects.create(name="White", hex_code="#FFFFFF")

        palette = Palette.objects.create(
            name="Cool Palette",
            description="Good Palette",
            primary=primary_color,
            secondary=secondary_color,
            third=third_color,
        )

        assert palette.name == "Cool Palette"
        assert palette.description == "Good Palette"
        assert palette.primary == primary_color
        assert palette.secondary == secondary_color
        assert palette.third == third_color
        assert str(palette) == "Palette Cool Palette"


@pytest.mark.django_db
class TestProfile:
    def test_profile_creation(self):
        user = User.objects.create(username="testuser")
        profile = Profile.objects.create(user=user)

        assert profile.user == user
        assert str(profile) == "testuser's Profile"


@pytest.mark.django_db
class TestUiSetting:
    def test_ui_setting_creation(self):
        user = User.objects.create(username="testuser")
        profile = Profile.objects.create(user=user)

        color = Color.objects.create(name="Red", hex_code="#FF0000")
        palette = Palette.objects.create(
            name="Cool Palette",
            description="Good Pallete",
            primary=color,
            secondary=color,
            third=color,
        )

        ui_setting = UiSetting.objects.create(background_color=color, palette=palette)
        profile.ui_settings = ui_setting
        assert ui_setting.profile == profile
        assert ui_setting.background_color == color
        assert ui_setting.palette == palette
        assert str(ui_setting) == f"{profile.user.username}'s UI Settings"
