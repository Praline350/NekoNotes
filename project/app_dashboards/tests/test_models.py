import pytest
from django.contrib.auth import get_user_model
from app_dashboards.models import Dashboard

User = get_user_model()


@pytest.mark.django_db  # Cette annotation permet d'accéder à la base de données
class TestDashboard:

    def test_dashboard_creation(self):
        user = User.objects.create(username="testuser")
        dashboard = Dashboard.objects.create(user=user)

        assert dashboard.user == user
        assert str(dashboard) == "testuser's Dashboard"
