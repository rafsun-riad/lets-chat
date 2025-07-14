from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Category, Channel


@receiver(pre_delete, sender=Category)
def category_icon_delete(sender, instance, **kwargs):
    if instance.icon:
        instance.icon.delete(save=False)


@receiver(pre_delete, sender=Channel)
def channel_icon_banner_delete(sender, instance, **kwargs):
    if instance.icon:
        instance.icon.delete(save=False)
    if instance.banner:
        instance.banner.delete(save=False)
