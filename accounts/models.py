from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    is_host = models.BooleanField(default=False)
    # host_requested=models.BooleanField(default=False)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    def _str_(self):
        return self.email

class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist_profile')
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artist_profiles/', blank=True, null=True)

    def _str_(self):
        return self.user.get_full_name() #or self.user.username
