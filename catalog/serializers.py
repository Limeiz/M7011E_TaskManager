from rest_framework import serializers

from .models import User, Task, List, Reminder, Achievement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class TaskSerializer(serializers.ModelSerializer):
    task_slug = serializers.SlugRelatedField(
        read_only=True,
        source='task',
        slug_field='slug'
    )

    task = serializers.HyperlinkedRelatedField(
        view_name='task:task_admin_details',
        read_only=True,
        lookup_field='slug'
    )

    priority = serializers.CharField(source='get_priority',
                                             read_only=True)

    status = serializers.CharField(source='get_status',
                                             read_only=True)
    assignee = serializers.CharField(source='get_username',
                                             read_only=True)
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'file', 'priority', 'deadline',
                  'status', 'slug', 'task_slug', 'task', 'assignee']



class ReminderSerializer(serializers.ModelSerializer):
    reminder_slug = serializers.SlugRelatedField(
        read_only=True,
        source='reminder',
        slug_field='slug'
    )

    reminder = serializers.HyperlinkedRelatedField(
        view_name='reminder:reminder_admin_details',
        read_only=True,
        lookup_field='slug'
    )

    class Meta:
        model = Reminder
        fields = ['task_id', 'username', 'date', 'slug', 'reminder_slug',
                  'reminder']


class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ListSerializer(serializers.ModelSerializer):
    assigned_users = UserUsernameSerializer(many=True)
    assigned_tasks = TaskSerializer(many=True)

    list_slug = serializers.SlugRelatedField(
        read_only=True,
        source='list',
        slug_field='slug'
    )

    list = serializers.HyperlinkedRelatedField(
        view_name='list:list_admin_details',
        read_only=True,
        lookup_field='slug'
    )

    class Meta:
        model = List
        fields = 'list_name', 'slug', 'list_slug', 'list', 'assigned_users', 'assigned_tasks'


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
