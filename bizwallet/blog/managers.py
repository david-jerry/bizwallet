from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone


class PostManager(models.Manager):
    def get_queryset(self):
        # All posts
        return super().get_queryset()

    def all_posts(self):
        # All posts
        return super().get_queryset().filter(status="published")

    def recent_posts(self):
        # All posts
        return super().get_queryset().filter(status="published").order_by("-pub_date")[:5]

    def all_draft(self):
        # All drafted posts
        return super().get_queryset().filter(status="draft")
