from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import models
from six import python_2_unicode_compatible


class BaseProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    slug = models.UUIDField(default=uuid.uuid4, blank=True, editable=False)
    # Add more user profile fields here. Make sure they are nullable
    # or with default values
    # TODO: change to push to GCS
    picture = models.ImageField(
        "Profile picture", upload_to="profile_pics/%Y-%m-%d/", null=True, blank=True
    )
    bio = models.CharField("Short Bio", max_length=200, blank=True, null=True)
    email_verified = models.BooleanField("Email verified", default=False)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Profile(BaseProfile):
    def __str__(self):
        return "{first_name}'s profile".format(first_name=self.user)
