from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    default_auto_field = "django.db.models.BigAutoField"

    is_administrator = models.BooleanField(default=False)
    is_advisor = models.BooleanField(default=False)
    name = models.CharField("Name", max_length=100)
