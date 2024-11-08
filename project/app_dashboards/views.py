from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import View
from django.contrib import messages

from .models import *


@method_decorator(login_required, name="dispatch")
class HomeView(View):
    template_name = "dashboard/home.html"

    def get(self, request):
        dashboard = Dashboard.objects.get(user=request.user)
        widgets = dashboard.widgets.all()
        for widget in widgets:
            print(widget.name)
        context = {
            "widgets": widgets,
        }
        return render(request, self.template_name, context=context)
