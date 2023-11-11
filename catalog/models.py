from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20, help_text='Enter name')

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.self.name
