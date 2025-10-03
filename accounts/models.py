from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings


class User(AbstractUser):
    is_host = models.BooleanField(default=False)
    # host_requested=models.BooleanField(default=False)


    def _str_(self):
        return self.email


