from rest_framework import serializers
from .models import User, Task, Reminder, List


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'file', 'priority', 'deadline', 'status']


class ReminderSerializer(serializers.ModelSerializer):
    #task = TaskSerializer()
    #user = UserSerializer()

    class Meta:
        model = Reminder
        fields = ['task_id', 'username', 'date']

class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ListSerializer(serializers.ModelSerializer):
    assigned_users = UserUsernameSerializer(many=True)
    assigned_tasks = TaskSerializer(many=True)

    class Meta:
        model = List
        fields = '__all__'
