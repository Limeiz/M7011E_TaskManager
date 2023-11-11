from django.db import models
from django.urls import reverse

# Create your models here.

class User(models.Model):
    """Model representing a user."""
    __tablename__ = 'user'
    username = models.CharField(max_length=50, help_text="Enter a username")

    class Meta:
        ordering = ["username"]

    def __str__(self):
        """String for representing the Model object."""
        return self.username

    def get_absolute_url(self):
        """Returns the url to access a particular username instance."""
        return reverse('genre-detail', args=[str(self.id)])

class Task(models.Model):
    """Model representing a task."""
    __tablename__ = 'task'
    task_name = models.CharField(max_length=50, help_text="Enter a task")

    class Meta:
        ordering = ["task name"]

    def __str__(self):
        """String for representing the Model object."""
        return self.task_name

    def get_absolute_url(self):
        """Returns the url to access a particular username instance."""
        return reverse('genre-detail', args=[str(self.id)])

class Reminder(models.Model):
    """Model representing a reminder."""
    __tablename__ = 'reminder'
    reminder_id = models.DateField(max_length=50, help_text="Enter a reminder")

    class Meta:
        ordering = ["reminder_id"]

    def __str__(self):
        """String for representing the Model object."""
        return self.reminder_id

    def get_absolute_url(self):
        """Returns the url to access a particular username instance."""
        return reverse('genre-detail', args=[str(self.id)])


class List(models.Model):
    """Model representing a list."""
    __tablename__ = 'list'
    list_id = models.CharField(max_length=50, help_text="Enter a list")

    class Meta:
        ordering = ["list_id"]

    def __str__(self):
        """String for representing the Model object."""
        return self.list_id

    def get_absolute_url(self):
        """Returns the url to access a particular username instance."""
        return reverse('genre-detail', args=[str(self.id)])

class ListEntry(models.Model):
    """Model representing a list entry."""
    __tablename__ = 'listEntry'
    listentry_id = models.CharField(max_length=50, help_text="Enter a list entry")

    class Meta:
        ordering = ["listentry_id"]

    def __str__(self):
        """String for representing the Model object."""
        return self.listentry_id

    def get_absolute_url(self):
        """Returns the url to access a particular username instance."""
        return reverse('genre-detail', args=[str(self.id)])


class SharedList(models.Model):
    """Model representing a shared list."""
    __tablename__ = 'sharedList'
    sharedlist_id = models.CharField(max_length=50, help_text="Enter a shared list")

    class Meta:
        ordering = ["sharedlist_id"]

    def __str__(self):
        """String for representing the Model object."""
        return self.sharedlist_id

    def get_absolute_url(self):
        """Returns the url to access a particular username instance."""
        return reverse('genre-detail', args=[str(self.id)])


class Group(models.Model):
    """Model representing a group."""
    __tablename__ = 'group'
    group_id = models.CharField(max_length=50, help_text="Enter a group")

    class Meta:
        ordering = ["group_id"]

    def __str__(self):
        """String for representing the Model object."""
        return self.group_id

    def get_absolute_url(self):
        """Returns the url to access a particular username instance."""
        return reverse('genre-detail', args=[str(self.id)])

class GroupEntry(models.Model):
    """Model representing a group entry."""
    __tablename__ = 'groupEntry'
    groupentry_id = models.CharField(max_length=50, help_text="Enter a group entry")

    class Meta:
        ordering = ["groupentry_id"]

    def __str__(self):
        """String for representing the Model object."""
        return self.groupentry_id

    def get_absolute_url(self):
        """Returns the url to access a particular username instance."""
        return reverse('genre-detail', args=[str(self.id)])
