import os
import random

import readtime
from category.models import Category, Tag
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import (
    CASCADE,
    SET_NULL,
    BigIntegerField,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    ImageField,
    IntegerField,
    ManyToManyField,
    OneToOneField,
    PositiveSmallIntegerField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
# Third party installs
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

from .managers import PostManager

# from .validators import file_validator

# REGEX Expressions for validation
SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NUM_REGEX = "^[0-9]*$"
ABC_REGEX = "^[A-Za-z]*$"


# Image upload folders
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def blog_file_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "posts_videos/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )

def post_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "posts/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


User = settings.AUTH_USER_MODEL

# Create your models here.
class Post(TimeStampedModel):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS = (
        (DRAFT, "Draft"),
        (PUBLISHED, "Published")
    )
    pub_date = DateField(
        _("Post Published Date"),
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=False,
    )
    title = CharField(_("Post Title"), max_length=500, blank=True, null=True, unique=True)
    slug = SlugField(max_length=700, blank=True, null=True, unique=True)
    author = ForeignKey(User, on_delete=SET_NULL, related_name="blogpost", null=True)
    content = HTMLField(_("Post Content"), null=True, blank=True)
    videos = FileField(
        _("Upload Video"),
        upload_to=blog_file_path,
        null=True,
        blank=True,
        # validators=[file_validator],
    )
    url = URLField(blank=True, max_length=500, null=True, unique=True)
    tags = ManyToManyField("category.Tag", help_text="Tag this item.")
    status = CharField(_("Status"), max_length=100, blank=True, null=True, choices=STATUS, default=DRAFT)
    featured = BooleanField(default=False)
    objects = PostManager()

    def __str__(self):
        return self.title

    @property
    def readtime(self):
        return str(readtime.of_test(self.content))

    @property
    def get_related_posts_by_tags(self):
        return Post.objects.filter(tags__in=self.tags.all())[:4]


    @property
    def get_recent_posts(self):
        return Post.objects.order_by('-created_at')[:5]


    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def get_image_url(self):
        img = self.image_set.first()
        if img:
            return img.image.url
        return img #None

    class Meta:
        managed = True
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created", "-modified"]

    def get_absolute_url(self):
        """Get url for blog's detail view.

        Returns:
            str: URL for blog detail.

        """
        return reverse("blogs:detail", kwargs={"slug": self.slug})


    def get_update_url(self):
        return f"{self.get_absolute_url}/update"

    def get_delete_url(self):
        return f"{self.get_absolute_url}/delete"



class Image(TimeStampedModel):
    post = ForeignKey(Post, on_delete=CASCADE)
    image = ResizedImageField(
        _("Upload Post Image"), quality=75, force_format='JPEG', size=[1920, 1148], crop=['middle', 'center'], upload_to=post_image, null=True, blank=True
    )

    def __str__(self):
        return self.post.title

    class Meta:
        managed = True
        verbose_name = "Post Files"
        verbose_name_plural = "Post Files"
        ordering = ["-created"]

