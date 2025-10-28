# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# -------------------------
# Custom User Model
# -------------------------
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        blank=True,
        null=True
    )
    social_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.username


# -------------------------
# Profile Model
# -------------------------
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, null=True)
    social_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# -------------------------
# Notification Model
# -------------------------
class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"


# -------------------------
# Signals: Auto-create Profile when CustomUser is created
# -------------------------
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
