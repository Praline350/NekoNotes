import logging
import json

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import View
from django.contrib import messages


from app_dashboards.models import Dashboard
from .models import *
from .forms import *


# Récupérer le logger personnalisé
logger = logging.getLogger("custom_logger")


@method_decorator(login_required, name="dispatch")
class WidgetMaker(View):

    def post(self, request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                widget_name = data.get("widget_name")
                widget_html = self.create_widget(request, widget_name)
                if widget_html:
                    logger.info(f"Widget '{widget_name}' créé avec succès.")
                    return JsonResponse({"widget_html": widget_html})
                else:
                    logger.warning(f"Widget '{widget_name}' non trouvé.")
                    return JsonResponse({"error": "Widget not found"}, status=404)
            except json.JSONDecodeError as e:
                logger.error(f"Erreur lors du parsing JSON : {e}")
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            except Exception as e:
                logger.exception(f"Erreur inattendue lors de la requête POST : {e}")
                return JsonResponse({"error": "Internal server error"}, status=500)

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        widget_id = data.get("widget_id")
        try:
            widget = Dashboard.objects.get_widget(widget_id=widget_id)
            if widget:
                widget.delete()
                return JsonResponse({"success": True})
            else:
                logger.warning(f"Widget avec ID {widget_id} non trouvé.")
                return JsonResponse({"success": False, "error": "widget not found"})
        except Dashboard.DoesNotExist:
            logger.error(f"Dashboard non trouvé pour widget_id : {widget_id}")
            return JsonResponse({"success": False, "error": "Dashboard not found"})
        except json.JSONDecodeError as e:
            logger.error(f"Erreur lors du parsing JSON : {e}")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            logger.exception(f"Erreur inattendue lors de la requête DELETE : {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    def create_widget(self, request, widget_name):
        match widget_name:
            case "Simple Todo List":
                return self.create_simple_todo_list(request)
            case _:
                logger.warning(f"Widget '{widget_name}' non implémenté.")
                return None

    def create_simple_todo_list(self, request):
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
            logger.error(f"Dashboard introuvable pour l'utilisateur {request.user}.")
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
            widget = Dashboard.objects.get_widget(widget_id=widget_id)
            widget.title = new_title
            widget.save()
            return JsonResponse({"success": True})
        except Widget.DoesNotExist:
            logger.error(f"Widget introuvable pour l'utilisateur {request.user}.")
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
            logger.warning(
                f"Le widget est introuvable pour l'utilisatuer {request.user}"
            )
            return JsonResponse(
                {"success": False, "error": "TodoList non trouvée"}, status=404
            )
        except Exception as e:
            logger.exception(f"Erreur inattendue lors de la requête POST : {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def put(self, request, *args, **kwargs):
        """
        Handle task updates (HTTP PUT for updating title or status).
        """
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")

            if not task_id:
                logger.warning(
                    f"La tache est introuvable pour l'utilisateur {request.user}"
                )
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
                logger.warning(
                    f"Erreur lors de la récupération du titre de la tache {task.id}"
                )
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
            logger.warning(
                f"La tache est introuvable pour l'utilisatuer {request.user}"
            )
            return JsonResponse({"success": False, "error": "Task not found"})
        except json.JSONDecodeError as e:
            logger.error(f"Erreur lors du parsing JSON : {e}")
            return JsonResponse({"success": False, "error": "Invalid JSON"})
