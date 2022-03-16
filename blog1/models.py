from ssl import create_default_context
from typing import Tuple
from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    auth = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='+')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

