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

    def connect_and_get_csrf(self):
        self.client.login(username="testuser", password="securepassword123")
        self.client.get(reverse("home"))
        self.csrf_token = self.client.cookies["csrftoken"].value

    def test_make_widget(self):
        self.connect_and_get_csrf()
        response = self.client.post(
            reverse("widget_manager"),
            data={"widget_name": "Simple Todo List"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        # Vérification de la réponse
        assert response.status_code == 200  # Vérifie que le code de statut est 200

    def test_make_widget_with_invalid_name(self):
        self.connect_and_get_csrf()
        response = self.client.post(
            reverse("widget_manager"),
            data={"widget_name": "Error"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        assert (
            response.json().get("error") == "Widget not found"
        ), "Error message mismatch"

    def test_make_widget_exceptions(self):
        self.connect_and_get_csrf()
        response = self.client.post(
            reverse("widget_manager"),
            data="not a json",
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert (
            response.json().get("error") == "Invalid JSON format"
        ), "Error message mismatch"

    def test_delete_widget(self):
        self.connect_and_get_csrf()
        response = self.client.delete(
            reverse("widget_manager"),
            data={"widget_id": self.widget.id},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        assert response.status_code == 200
        assert not SimpleTodoList.objects.filter(id=self.widget.id).exists()

    def test_delete_widget_error(self):
        self.connect_and_get_csrf()
        response = self.client.delete(
            reverse("widget_manager"),
            data={"widget_id": 999},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )
        assert response.status_code == 404

        response = self.client.delete(
            reverse("widget_manager"),
            data="Not a json",
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        assert response.status_code == 400

    def test_simpletodo_update(self):
        self.connect_and_get_csrf()
        response = self.client.put(
            reverse("simple_todo_manager"),
            data={"widget_id": self.widget.id, "new_title": "update title"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        assert response.status_code == 200
        self.widget.refresh_from_db()
        assert self.widget.title == "update title"

    def test_simpletodo_exception(self):
        self.connect_and_get_csrf()
        response = self.client.put(
            reverse("simple_todo_manager"),
            data={"widget_id": 99, "new_title": "update title"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        assert response.status_code == 404

        response = self.client.put(
            reverse("simple_todo_manager"),
            data="not json",
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        assert response.status_code == 400


@pytest.mark.django_db
class TestTaskView:
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="securepassword123"
        )
        self.dashboard = Dashboard.objects.create(user=self.user)
        self.widget = SimpleTodoList.objects.create(dashboard=self.dashboard)

    def connect_and_get_csrf(self):
        self.client.login(username="testuser", password="securepassword123")
        self.client.get(reverse("home"))
        self.csrf_token = self.client.cookies["csrftoken"].value

    def test_make_task(self):
        self.connect_and_get_csrf()
        response = self.client.post(
            reverse("task"),
            data={"widget_id": self.widget.id, "title": "new task"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        assert response.status_code == 200
        assert Task.objects.count() == 1
        task = Task.objects.first()
        assert task.title == "new task"

    def test_task_update(self):
        task = Task.objects.create(title="task")
        self.connect_and_get_csrf()
        response = self.client.put(
            reverse("task"),
            data={"task_id": task.id, "title": "new title"},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        assert response.status_code == 200
        task.refresh_from_db()
        assert task.title == "new title"

        response = self.client.put(
            reverse("task"),
            data={"task_id": task.id, "status": False},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        assert response.status_code == 200
        task.refresh_from_db()
        assert task.completed == False

    def test_task_delete(self):
        task = Task.objects.create(title="task")
        self.connect_and_get_csrf()
        response = self.client.delete(
            reverse("task"),
            data={"task_id": task.id},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        assert response.status_code == 200
        assert not Task.objects.filter(id=task.id).exists()
