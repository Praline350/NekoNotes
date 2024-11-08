from rest_framework import serializers
from .models import Task, SimpleTodoList


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class SimpleTodoListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = SimpleTodoList
        fields = "__all__"
