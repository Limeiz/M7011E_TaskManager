from django.contrib import admin
from .models import Task, List, Reminder




@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'priority', 'status', 'deadline')


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('reminder_id', 'task_id', 'username', 'date')


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('list_id', 'list_name', 'assigned_users_display', 'assigned_tasks_display')

    def assigned_users_display(self, obj):
        return ', '.join([user.username for user in obj.assigned_users.all()])

    assigned_users_display.short_description = 'Assigned Users'

    def assigned_tasks_display(self, obj):
        return ', '.join([f"{task.task_name}" for task in obj.assigned_tasks.all()])

    assigned_tasks_display.short_description = 'Assigned Tasks'
