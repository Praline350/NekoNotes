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

    def test_dashboard_all_widgets(self):
        dashboard = Dashboard.objects.create(user=self.user)
        widget_a = EmptyWidget.objects.create(dashboard=dashboard, name="widgetA")
        widget_b = EmptyWidget.objects.create(dashboard=dashboard)
        widgets = dashboard.widgets.all()

        assert len(widgets) == 2
        assert widget_a in widgets
        assert widget_b in widgets
        assert str(widget_a) == "widgetA"

    def test_dashboard_manager(self):
        dashboard = Dashboard.objects.create(user=self.user)
        widget_a = EmptyWidget.objects.create(dashboard=dashboard, name="widgetA")

        widget = Dashboard.objects.get_widget(widget_id=widget_a.id)
        false_result = Dashboard.objects.get_widget(widget_id=9999)

        assert widget.name == "widgetA"

        assert false_result is None
