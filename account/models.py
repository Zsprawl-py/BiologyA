from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    verified = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'