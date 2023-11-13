from django.contrib import admin
from .models import User, Task, Reminder, List, ListEntry, Group, GroupEntry, SharedList

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Reminder)
admin.site.register(List)
admin.site.register(ListEntry)
admin.site.register(Group)
admin.site.register(GroupEntry)
admin.site.register(SharedList)
