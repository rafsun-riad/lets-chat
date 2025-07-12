import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Account(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    # You can add additional fields here if needed
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, default="", null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(
        unique=True, max_length=100, default="", blank=True, null=True
    )

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.name = self.first_name + " " + self.last_name
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email if self.email else self.username
