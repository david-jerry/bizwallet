from django.db.models.signals import pre_save
from django.dispatch import receiver

from bizwallet.core.models import Services, ServicesVariations
from bizwallet.utils.unique_slug_generator import unique_slug_generator

@receiver(pre_save, sender=Services)
def create_service_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=ServicesVariations)
def create_servicevariation_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

