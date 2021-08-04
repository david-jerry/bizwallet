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
from dateutil import relativedelta
from django.contrib.auth import get_user_model
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
from django_resized import ResizedImageField
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

User = get_user_model()


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


class EmailSubscribe(TimeStampedModel):
    user = OneToOneField(User, on_delete=SET_NULL, null=True, blank=True)
    email = EmailField(_("Email Please"), required=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.fullname} just subscribed to the mailing list"

    class Meta:
        managed = True
        verbose_name = "Email Subscriber"
        verbose_name_plural = "Email Subscribers"
        ordering = ["-created", "-modified"]

class Services(TimeStampedModel):
    """services in bizwallet."""

    image = ResizedImageField(size=[2000, 1222], default='images/team/7.jpg', quality=75, crop=['middle', 'center'], upload_to=services_image, force_format='JPEG')
    title = CharField(
        _("Service Title"), max_length=500, blank=True, null=True,
    )
    slug = SlugField(_('Service Slug'), max_length=500, unique=True, null=True, blank=True)
    description = HTMLField(_("Service Description"),null=True, blank=True)
    active = BooleanField(_("Activate Services"), default=False)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("services:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["-created", "-modified"]




class ServicesVariations(TimeStampedModel):
    DURATION = (
        ("0", "0"),
        ("28", "28"),
        ("64", "64"),
        ("112", "112"),
        ("168", "168"),
        ("336", "336"),
        ("672", "672")
    )
    service = ForeignKey(Services, on_delete=CASCADE, related_name="servicevariation")
    title = CharField(
        _("Service Title"), max_length=500, blank=True, null=True,
    )
    slug = SlugField(_('Variation Slug'), max_length=500, unique=True, null=True, blank=True)
    min_investment = DecimalField(
        _("Minimum & Maximum Investment Amount"), decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('50000.00')), MaxValueValidator(Decimal('2000000.00'))], help_text="min-amount: ₦50,000.00, max-amount: ₦2,000,000.00", null=True, blank=True
    )
    percentage = DecimalField(_("Variation Percentage"), max_digits=3, decimal_places=2, null=True, blank=True, default=1.0, help_text="1.00 means 100%, 0.50 mean 50%")
    duration = CharField(_("Duration"), max_length=4, choices=DURATION, null=True, blank=True, default="168")
    active = BooleanField(_("Activate Variation"), default=False)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = "ServicesVariation"
        verbose_name_plural = "ServicesVariations"
        ordering = ["-created", "-modified"]


