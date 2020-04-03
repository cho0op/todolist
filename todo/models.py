from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField(blank=True)
    creating_date = models.DateTimeField(auto_now_add=True)
    completing_date=models.DateTimeField(null=True, blank=True)
    importance=models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.title

# Create your models here.
