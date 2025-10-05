from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
# from django.conf import settings


class User(AbstractUser):
    is_host = models.BooleanField(default=False)
    # host_requested=models.BooleanField(default=False)
    email=models.EmailField(unique=True)
    profile_image=models.ImageField(upload_to='profiles/',default='profiles/default.png')
    notify_on_event=models.BooleanField(default=True)

    def _str_(self):
        return self.email


