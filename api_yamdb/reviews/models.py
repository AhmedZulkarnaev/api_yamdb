from django.db import models
from django.contrib.auth.models import AbstractUser

CHOICES = [('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')]


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=CHOICES, default='user')
    confirmation_code = models.PositiveIntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    password = None

    def __str__(self):
        return self.username
