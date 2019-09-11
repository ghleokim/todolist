from django.db import models

# Create your models here.
class Post(models.Model):
    schedule = models.CharField(max_length=100)
    due_date = models.DateTimeField()