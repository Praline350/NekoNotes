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


@csrf_exempt  # Désactive temporairement CSRF pour simplifier le test, mais pas recommandé pour la production
def add_simple_todo_list(request):
    if request.method == "POST":
        print("Données brutes reçues :", request.body)
        try:
            data = json.loads(request.body)
            print(data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        title = data.get("title")

        if not title:
            return JsonResponse({"error": "title is required"}, status=400)

        dashboard = Dashboard.objects.filter(user=request.user).first()
        if dashboard:
            todo_list = SimpleTodoList(title=title, dashboard=dashboard)
            todo_list.save()
            return JsonResponse({"message": "Simple TodoList created successfully"})
        else:
            return JsonResponse({"error": "No dashboard found"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)
