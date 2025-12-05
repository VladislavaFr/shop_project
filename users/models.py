from django.contrib.auth.models import AbstractUser
from django.db import models

def user_avatar_path(instance, filename):
    return f"avatars/user_{instance.id}/{filename}"

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username