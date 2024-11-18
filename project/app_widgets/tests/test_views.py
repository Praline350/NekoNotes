import pytest
import json
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from app_dashboards.models import Dashboard
from app_widgets.models import SimpleTodoList, Task

User = get_user_model()


@pytest.mark.django_db
class TestWidgetMaker:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="securepassword123"
        )
        self.dashboard = Dashboard.objects.create(user=self.user)
        self.widget = SimpleTodoList.objects.create(dashboard=self.dashboard)

    def test_make_widget(self):
        self.client.login(username="testuser", password="securepassword123")
        self.client.get(reverse("home"))
        csrf_token = self.client.cookies["csrftoken"].value
        response = self.client.post(
            reverse("widget_manager"),
            data={"widget_name": "Simple Todo List"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        # Vérification de la réponse
        assert response.status_code == 200  # Vérifie que le code de statut est 200
