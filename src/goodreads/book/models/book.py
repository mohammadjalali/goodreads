from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Book(models.Model):
    name = models.CharField(max_length=100)
    summery = models.TextField()
