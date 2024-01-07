from rest_framework import serializers

from .models import User, Task, List, Reminder, Achievement

class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.CharField(source='assignee.username') #read_only=True
    status = serializers.ChoiceField(choices=Task.TASK_STATUS,
                                     source='get_status_display')
    priority = serializers.ChoiceField(choices=Task.TASK_PRIORITY,
                                       source='get_priority_display')

    class Meta:
        model = Task
        fields = ['task_name', 'description', 'file', 'priority', 'deadline',
                  'status', 'assignee', 'slug']



class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['task_id', 'username', 'date', 'slug']


class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ListSerializer(serializers.ModelSerializer):
    assigned_users = UserUsernameSerializer(many=True)
    assigned_tasks = TaskSerializer(many=True)

    class Meta:
        model = List
        fields = ('list_name', 'slug', 'assigned_users',
                  'assigned_tasks')


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
