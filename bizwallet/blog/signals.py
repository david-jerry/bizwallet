from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from bizwallet.utils.unique_slug_generator import unique_slug_generator

from .models import Post


@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance, *args, **kwargs):
	if instance.title and not instance.slug:
		instance.slug = unique_slug_generator(instance)


