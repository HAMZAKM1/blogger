from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# users/models.py

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)
    social_link = models.URLField(blank=True, null=True)
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"