from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import ROLE_CHOICES, ROLE_VIEWER


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_VIEWER,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username