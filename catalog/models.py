from django.db import models
from django.urls import reverse

class User(models.Model):
    __tablename__ = 'User'

    USER_TYPES = (
        ('u', 'User'),
        ('a', 'Admin'),
        ('s', 'Super User'),
    )

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPES, default='u')
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


class Task(models.Model):
    __tablename__ = 'Task'

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
    task_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    file = models.FileField(blank=True)
    priority = models.CharField(max_length=1, choices=TASK_PRIORITY, blank=True, help_text='Task priority')
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=TASK_STATUS, default='t', help_text='Task status')

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"{self.task_name}"

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])


class Reminder(models.Model):
    __tablename__ = 'Reminder'
    reminder_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    task_name = models.ForeignKey(Task, to_field='task_name', on_delete=models.RESTRICT)
    user_name = models.ForeignKey(User, to_field='username', on_delete=models.RESTRICT)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.reminder_id}"

    def get_absolute_url(self):
        return reverse('reminder-detail', args=[str(self.id)])

class List(models.Model):
    __tablename__ = 'List'
    list_id = models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=200, unique=True)
    assigned_users = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.list_name}"

    def get_absolute_url(self):
        return reverse('list-detail', args=[str(self.id)])


class ListEntry(models.Model):
    """Model representing a list entry."""
    __tablename__ = 'ListEntry'
    listentry_id = models.AutoField(primary_key=True)
    assigned_tasks = models.ManyToManyField(Task)
    list_name = models.ForeignKey(List, to_field='list_name', on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.listentry_id}"

    def get_absolute_url(self):
        return reverse('listentry-detail', args=[str(self.id)])
