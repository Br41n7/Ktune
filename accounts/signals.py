from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, ArtistProfile

@receiver(post_save, sender=User)
def create_artist_profile(sender, instance, created, **kwargs):
    if created and instance.is_host:  # or some other condition
        ArtistProfile.objects.create(user=instance)
