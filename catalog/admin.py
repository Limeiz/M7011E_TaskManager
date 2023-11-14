from django.contrib import admin
from .models import User, Task, Reminder, List, ListEntry
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
   list_display = ('user_id', 'username', 'email', 'is_logged_in')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
   list_display = ('task_id', 'task_name', 'priority', 	'status', 'deadline')


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
   list_display = ('reminder_id', 'task_name', 'user_name', 'date')


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('list_name', 'assigned_users_display')

    def assigned_users_display(self, obj):
        return ', '.join([user.username for user in obj.assigned_users.all()])
    assigned_users_display.short_description = 'Assigned Users'
@admin.register(ListEntry)
class ListEntryAdmin(admin.ModelAdmin):
   list_display = ('list_name', 'assigned_tasks_display')

   def assigned_tasks_display(self, obj):
       return ', '.join([task.task_name for task in obj.assigned_tasks.all()])

   assigned_tasks_display.short_description = 'Assigned Tasks'