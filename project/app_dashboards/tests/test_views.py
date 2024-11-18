import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

from app_dashboards.models import Dashboard, EmptyWidget
from app_widgets.models import SimpleTodoList


@pytest.mark.django_db
class TestHomeView:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="securepassword123"
        )
        self.dashboard = Dashboard.objects.create(user=self.user)

    def test_home_view(self):
        widget = SimpleTodoList.objects.create(dashboard=self.dashboard, name="widgetA")
        login_succes = self.client.login(
            username="testuser", password="securepassword123"
        )
        widgets = self.dashboard.widgets.all()
        for w in widgets:
            print(w)
        response = self.client.get(reverse("home"))

        assert login_succes is True
        assert response.status_code == 200
        assert response.wsgi_request.user.is_authenticated
