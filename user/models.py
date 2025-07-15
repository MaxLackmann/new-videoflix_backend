from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomerUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        The given username and email will be set to the new user, and the
        given password will be set as the user's password. The user's
        is_staff and is_superuser flags will be set to True; is_active will
        be set to True unless no_homepage is True.
        Returns the User object of the newly created user.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return super().create_superuser(username, email, password, **extra_fields)

class CustomerUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    objects = CustomerUserManager() 

    def __str__(self):
        return self.email

