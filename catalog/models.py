from django.db import models
from django.urls import reverse


class User(models.Model):
    __tablename__ = 'User'
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return self.username

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
    task_name = models.CharField(max_length=200)
    note = models.TextField(blank=True)
    file = models.FileField(blank=True)
    priority = models.CharField(max_length=1, choices=TASK_PRIORITY, blank=True, help_text='Task priority')
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=TASK_STATUS, default='t', help_text='Task status')

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.task_name

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])


class Reminder(models.Model):
    __tablename__ = 'Reminder'
    reminder_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    task_id = models.ForeignKey(Task, on_delete=models.RESTRICT)
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.reminder_id

    def get_absolute_url(self):
        return reverse('reminder-detail', args=[str(self.id)])


class List(models.Model):
    __tablename__ = 'List'
    list_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.list_id

    def get_absolute_url(self):
        return reverse('list-detail', args=[str(self.id)])


class ListEntry(models.Model):
    """Model representing a list entry."""
    __tablename__ = 'ListEntry'
    listentry_id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey(Task, on_delete=models.RESTRICT)
    list_id = models.ForeignKey(List, on_delete=models.RESTRICT)

    def __str__(self):
        return self.listentry_id

    def get_absolute_url(self):
        return reverse('listentry-detail', args=[str(self.id)])


class Group(models.Model):
    __tablename__ = 'Group'
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=200)

    class Meta:
        ordering = ["group_name"]

    def __str__(self):
        return self.group_id

    def get_absolute_url(self):
        return reverse('group-detail', args=[str(self.id)])


class GroupEntry(models.Model):
    __tablename__ = 'GroupEntry'
    groupentry_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    group_id = models.ForeignKey(Group, on_delete=models.RESTRICT)

    def __str__(self):
        return self.groupentry_id

    def get_absolute_url(self):
        return reverse('groupentry-detail', args=[str(self.id)])


class SharedList(models.Model):
    __tablename__ = 'SharedList'
    sharedlist_id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(Group, on_delete=models.RESTRICT)
    list_id = models.ForeignKey(List, on_delete=models.RESTRICT)

    def __str__(self):
        return self.sharedlist_id

    def get_absolute_url(self):
        return reverse('sharedList-detail', args=[str(self.id)])
