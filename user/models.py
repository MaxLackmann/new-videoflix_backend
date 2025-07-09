from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomerUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
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

