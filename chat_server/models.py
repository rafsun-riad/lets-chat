import uuid

from django.conf import settings
from django.db import models

# Create your models here.


class Category(models.Model):
    """Model representing a category for organizing servers."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to="category_icons/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                existing = Category.objects.get(pk=self.pk)
                if existing.icon and self.icon != existing.icon:
                    existing.icon.delete(save=False)
            except Category.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Server(models.Model):
    """Model representing a server."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category"
    )
    description = models.TextField(blank=True, null=True)
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="server_member"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Channel(models.Model):
    """Model representing a channel within a server."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner"
    )
    topic = models.CharField(max_length=100, blank=True, null=True)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channel_server"
    )
    banner = models.ImageField(upload_to="channel_banners/", blank=True, null=True)
    icon = models.ImageField(upload_to="channel_icons/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                existing = Channel.objects.get(pk=self.pk)
                if existing.banner and self.banner != existing.banner:
                    existing.banner.delete(save=False)
                if existing.icon and self.icon != existing.icon:
                    existing.icon.delete(save=False)
            except Channel.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
