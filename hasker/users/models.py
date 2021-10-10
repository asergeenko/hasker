from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Hasker."""

    #: First and last name do not cover name patterns around the globe
    #username = models.CharField(_("Name of User"), max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    avatar = models.ImageField(default='avatars/default.jpg', upload_to='avatars/')

    #first_name = None  # type: ignore
    #last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
