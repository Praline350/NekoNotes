from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
import json
from django.views.generic import View
from django.contrib import messages


from app_dashboards.models import Dashboard
from .models import *
from .forms import *


@method_decorator(login_required, name="dispatch")
class WidgetMaker(View):

    def post(self, request):
        if request.method == "POST":
            data = json.loads(request.body)
            widget_name = data.get("widget_name")
            print(widget_name)
            widget_html = self.create_widget(request, widget_name)
            if widget_html:
                return JsonResponse({"widget_html": widget_html})
            else:
                return JsonResponse({"error": "Widget not found"}, status=404)

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        widget_id = data.get("widget_id")
        try:
            widget = Dashboard.objects.get_widget_by_id(widget_id=widget_id)
            if widget:
                widget.delete()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "widget not found"})
        except Dashboard.DoesNotExist:
            return JsonResponse({"success": False, "error": "dashboard not found"})

    def create_widget(self, request, widget_name):
        match widget_name:
            case "Simple Todo List":
                return self.create_simple_todo_list(request)
            case _:
                return None

    def create_simple_todo_list(self, request):
        print("creat simple list")
        dashboard = Dashboard.objects.filter(user=request.user).first()
        if dashboard:
            widget = SimpleTodoList.objects.create(dashboard=dashboard)
            widget_html = render(
                request,
                "components/widgets/simple_todo_list.html",
                {"widget": widget},
            ).content.decode("utf-8")
            return widget_html
        else:
            return JsonResponse(
                {"error": "Dashboard not found for the user"}, status=404
            )


class SimpleTodoWidget(View):
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(f"data json : {data}")
        widget_id = data.get("widget_id")
        new_title = data.get("new_title")
        try:
            widget = Dashboard.objects.get_widget_by_id(widget_id=widget_id)
            widget.title = new_title
            widget.save()
            return JsonResponse({"success": True})
        except Widget.DoesNotExist:
            return JsonResponse({"success": False, "error": "Widget not found"})


@method_decorator(login_required, name="dispatch")
class TaskView(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(f"data json : {data}")
        widget_id = data.get("widget_id")
        title = data.get("title")
        try:
            todo_list = SimpleTodoList.objects.get(id=widget_id)
            task = Task.objects.create(title=title)
            todo_list.tasks.add(task)
            task_html = render(
                request, "components/widgets/task.html", context={"task": task}
            ).content.decode("utf-8")
            return JsonResponse({"task_html": task_html})
        except SimpleTodoList.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "TodoList non trouvée"}, status=404
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def put(self, request, *args, **kwargs):
        """
        Handle task updates (HTTP PUT for updating title or status).
        """
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")

            if not task_id:
                return JsonResponse(
                    {"success": False, "error": "Missing task_id"}, status=400
                )

            task = Task.objects.get(id=task_id)

            # Dispatcher: update title or status
            if "title" in data:
                task.title = data["title"]
            elif "status" in data:
                task.completed = data["status"]
            else:
                return JsonResponse(
                    {"success": False, "error": "Missing title or status"}, status=400
                )

            task.save()
            return JsonResponse({"success": True})

        except Task.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Task not found"}, status=404
            )
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def delete(self, request, *args, **kwargs):
        """
        Handle task deletion (HTTP DELETE).
        """
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")

            if not task_id:
                return JsonResponse({"success": False, "error": "Missing task_id"})

            task = Task.objects.get(id=task_id)
            task.delete()
            return JsonResponse({"success": True})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"})
