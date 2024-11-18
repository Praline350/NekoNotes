import pytest
from django.contrib.auth import get_user_model
from app_dashboards.models import Dashboard, EmptyWidget

User = get_user_model()


@pytest.mark.django_db  # Cette annotation permet d'accéder à la base de données
class TestDashboard:
    def setup_method(self):
        self.user = User.objects.create(username="testuser")

    def test_dashboard_creation(self):
        dashboard = Dashboard.objects.create(user=self.user)

        assert dashboard.user == self.user
        assert str(dashboard) == "testuser's Dashboard"

    def test_dahsboard_manager_model(self):
        dashboard = Dashboard.objects.create(user=self.user)
        dashboard_manager = Dashboard.objects.get(id=dashboard.id)
        widget_a = EmptyWidget.objects.create(dashboard=dashboard)
        widget_b = EmptyWidget.objects.create(dashboard=dashboard)
        widgets = dashboard_manager.get_widgets(dashboard)

        assert len(widgets) == 2
        assert widget_a in widgets
        assert widget_b in widgets
