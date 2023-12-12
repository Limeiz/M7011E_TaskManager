from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    TASK_STATUS = (
        ('t', 'To do'),
        ('i', 'In progress'),
        ('d', 'Done'),
    )

    TASK_PRIORITY = (
        ('l', 'Low'),
        ('m', 'Medium'),
        ('h', 'High')
    )

    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='files/',
                            null=True,
                            blank=True)
    priority = models.CharField(max_length=1, choices=TASK_PRIORITY,
                                blank=True, help_text='Task priority')
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=TASK_STATUS, default='t',
                              help_text='Task status')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 blank=True)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            blank=False,
                            null=True)

    class Meta:
        ordering = ['priority']

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.task_name}"


class Reminder(models.Model):
    reminder_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    task_id = models.ForeignKey(Task, to_field='task_id',
                                on_delete=models.RESTRICT)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            blank=False,
                            null=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.reminder_id}"


class List(models.Model):
    list_id = models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=200)
    assigned_users = models.ManyToManyField(User)
    assigned_tasks = models.ManyToManyField(Task)
    slug = models.SlugField(max_length=255,
                            unique=True,
                            blank=False,
                            null=True)

    def __str__(self):
        return f"{self.list_name}"

    def is_assigned_users(self, user):
        return user in self.assigned_users.all()

    def is_assigned_task(self, task):
        return task in self.assigned_tasks.all()

    def get_user_tasks(self, user):
        if user in self.assigned_users.all():
            return self.assigned_tasks.all()


class Achievement(models.Model):
    achievement_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    completed_by = models.ManyToManyField(User, related_name='achievements')

    def __str__(self):
        return self.name
