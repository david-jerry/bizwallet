from __future__ import absolute_import

from django.conf import settings

from bizwallet.blog.models import Post


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {"DEBUG": settings.DEBUG}

def recent_posts(_request):
    return {"recent_posts": Post.objects.recent_posts}
