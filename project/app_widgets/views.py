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


@csrf_exempt  # Si tu utilises un décorateur CSRF, n'oublie pas de le gérer
def update_widget_title(request):
    if request.method == "POST":

        data = json.loads(request.body)
        print(f"data json : {data}")
        widget_id = data.get("widget_id")
        new_title = data.get("new_title")
        print(f"widgeti : {widget_id}, title ; {new_title}")

        try:
            dashboard = Dashboard.objects.get(user=request.user)
            widget = dashboard.widgets.objects.get(id=widget_id)
            widget.title = new_title
            widget.save()
            return JsonResponse({"success": True})
        except Widget.DoesNotExist:
            return JsonResponse({"success": False, "error": "Widget not found"})

    return JsonResponse({"success": False, "error": "Invalid request method"})
