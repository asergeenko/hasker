from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse



class User(AbstractUser):
    """Default user for Hasker."""

    #: First and last name do not cover name patterns around the globe
    date_joined = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    avatar = models.ImageField(default='avatars/default.jpg', upload_to='avatars/')


    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
