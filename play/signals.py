from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Channel
from django.contrib.auth.models import User


# Create a channel for every new user
@receiver(post_save, sender=User)
def create_channel(sender, instance, created, **kwargs):
    if created:
        Channel.objects.create(user=instance, name=instance.username)
