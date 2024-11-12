import pytest
from django.contrib.auth import get_user_model
from app_dashboards.models import Dashboard
from app_widgets.models import Task, SimpleTodoList

User = get_user_model()


@pytest.mark.django_db
class TestTodoList:

    @pytest.fixture(autouse=True)
    def setup(self):
        # Cette méthode s'exécute avant chaque test
        self.user = User.objects.create(username="testuser")
        self.dashboard = Dashboard.objects.create(user=self.user)
        self.task1 = Task.objects.create(title="task test1")

    def test_todo_list_creation(self):
        title = "My todo list"
        todo_list = SimpleTodoList.objects.create(dashboard=self.dashboard, name=title)
        todo_list.tasks.add(self.task1)

        assert todo_list.name == title
        assert todo_list.dashboard.user == self.user
        assert todo_list.tasks.count() == 1

    def test_select_widget(self):
        title = "My todo list"
        todo_list = SimpleTodoList.objects.create(dashboard=self.dashboard, name=title)
        todo_list.tasks.add(self.task1)

        assert todo_list.name == title

        widgets = self.dashboard.widgets.all()
        for widget in widgets:
            print(f"Widget : {widget.id}, {widget.dashboard_id}")

        widget = Dashboard.objects.get_widgets(dashboard=self.dashboard)

        print(f"widget filter :  {widget}")

        widget = Dashboard.objects.get_widget_by_id(widget_id=todo_list.id)

        assert todo_list.name == widget.name
