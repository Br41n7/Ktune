from django.db import models
from accounts.models import User

class Artist(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='artist_images/', blank=True, null=True)

    def _str_(self):
        return self.name

class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True)  # e.g. Comedy, Music, Dance
    profile_picture = models.ImageField(upload_to='artist_profiles/', blank=True, null=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    def _str_(self):
        return self.stage_name or self.user.username
