from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, default="")
    adress = models.CharField(max_length=100, default="")
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
