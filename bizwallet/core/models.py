from __future__ import absolute_import

# development system imports
import datetime
import os
import random
import uuid
from datetime import date, timedelta
from decimal import Decimal

# Third partie imports
from countries_plus.models import Country
from django_resized import ResizedImageField
from dateutil import relativedelta
# django imports
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    GenericIPAddressField,
    ImageField,
    OneToOneField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField


# REGEX Expressions for validation
SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NUM_REGEX = "^[0-9]*$"
ABC_REGEX = "^[A-Za-z]*$"


# Image upload folders
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def services_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "service-photo/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


class Services(TimeStampedModel):
    """services in bizwallet."""

    image = ResizedImageField(size=[500, 300], default='images/team/7.jpg', quality=75, crop=['middle', 'center'], upload_to=services_image, force_format='JPEG')
    dob = DateField(_("Date of Birth"), blank=True, null=True)
    title = CharField(
        _("Service Title"), max_length=500, blank=True, null=True,
    )
    description = HTMLField(_("Service Description"),null=True, blank=True)
    active = BooleanField(_("Activate Services"), default=False)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("services:detail", kwargs={"title": self.title})
