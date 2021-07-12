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

# Developer defined imports
# from ..utils.validators import (
#     validate_uploaded_image_extension,
#     validate_uploaded_pdf_extension,
# )

SEX = (
    ("", "Gender"),
    ("Male", "MALE"),
    ("Female", "FEMALE"),
)

MARITAL = (
    ("", "Marital"),
    ("Single", "Single"),
    ("Married", "Married"),
    ("Divorced", "Divorced"),
    ("Seperated", "Seperated"),
)

STATES = (
    ("", "States"),
    ("Abia", "Abia"),
    ("Adamawa", "Adamawa"),
    ("Akwa Ibom", "Akwa Ibom"),
    ("Anambra", "Anambra"),
    ("Bauchi", "Bauchi"),
    ("Bayelsa", "Bayelsa"),
    ("Benue", "Benue"),
    ("Borno", "Borno"),
    ("Cross River", "Cross River"),
    ("Delta", "Delta"),
    ("Ebonyi", "Ebonyi"),
    ("Enugu", "Enugu"),
    ("Edo", "Edo"),
    ("Ekiti", "Ekiti"),
    ("Gombe", "Gombe"),
    ("Imo", "Imo"),
    ("Jigawa", "Jigawa"),
    ("Kaduna", "Kaduna"),
    ("Kano", "Kano"),
    ("Katsina", "Katsina"),
    ("Kebbi", "Kebbi"),
    ("Kogi", "Kogi"),
    ("Kwara", "Kwara"),
    ("Lagos", "Lagos"),
    ("Nasarawa", "Nasarawa"),
    ("Niger", "Niger"),
    ("Ogun", "Ogun"),
    ("Ondo", "Ondo"),
    ("Osun", "Osun"),
    ("Oyo", "Oyo"),
    ("Plateau", "Plateau"),
    ("Rivers", "Rivers"),
    ("Sokoto", "Sokoto"),
    ("Taraba", "Taraba"),
    ("Yobe", "Yobe"),
    ("Zamfara", "Zamfara"),
)


# REGEX Expressions for validation
SSN_REGEX = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4}\\d{4}$)"
NUM_REGEX = "^[0-9]*$"
ABC_REGEX = "^[A-Za-z]*$"


# Image upload folders
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def profile_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "user-profile-photo/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


MEMBERSHIP_CHOICES = (
    ("DIAMOND", "diamond"),
    ("GOLD", "gold"),
    ("BRONZE", "bronze"),
    ("FREE", "free"),
)


class User(AbstractUser):
    """Default user for bizwallet."""

    balance = DecimalField(
        default=0, max_digits=20, decimal_places=2, blank=True, null=True
    )
    ip = GenericIPAddressField(
        _("User IP"), protocol="both", unpack_ipv4=False, blank=False, null=True
    )
    image = ResizedImageField(size=[500, 300], default='images/team/7.jpg', quality=75, crop=['middle', 'center'], upload_to=profile_image, force_format='JPEG')
    gender = CharField(_("Gender"), max_length=7, blank=True, null=True, choices=SEX)
    dob = DateField(_("Date of Birth"), blank=True, null=True)
    marital = CharField(
        _("Marital Status"), max_length=10, blank=True, null=True, choices=MARITAL
    )
    phone_no = CharField(_("Phone Number"), blank=True, null=True, max_length=13)
    country = CharField(_("User Country"), blank=False, null=True, max_length=50)
    city = CharField(_("Located City"), max_length=50, null=True, blank=True)
    state = CharField(
        _("State of Origin"), max_length=15, blank=True, null=True, choices=STATES
    )
    address = CharField(
        _("Residntial Address"), max_length=600, null=True, blank=True, unique=True
    )
    is_field_worker = BooleanField(_("Are you a field worker"), default=True)
    has_paid = BooleanField(_("User has Paid"), default=False)
    accept_terms = BooleanField(_("Accept our terms"), default=False)

    def initials(self):
        fname = self.first_name[0].upper()
        lname = self.last_name[0].upper()
        return f"{fname} {lname}"

    @property
    def age(self):
        TODAY = datetime.date.today()
        if self.dob:
            return "%s" % relativedelta.relativedelta(TODAY, self.dob).years
        else:
            return None

    @property
    def fullname(self):
        if self.first_name and self.last_name:
            fullname = f"{self.first_name} {self.last_name}"
        else:
            fullname = f"{self.username}"
        return fullname

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


# class CEOBizwallet(TimeStampedModel):
#     user = OneToOneField(User, on_delete=CASCADE, related_name="ceoprofile")

#     def __str__(self):
#        return self.user.fullname

#     class Meta:
#         managed = True
#         verbose_name = 'CEOBizwallet'
#         verbose_name_plural = 'CEOBizwallets'
#         ordering = ['-created', '-modified']


class Membership(TimeStampedModel):
    slug = SlugField(null=True, blank=True, unique=True)
    title = CharField(choices=MEMBERSHIP_CHOICES, default="FREE", max_length=30)
    # activated = Boolean(default=False)
    # forced_expired = BooleanField(default=False)
    # expires = IntegerField(default=365) # 7 Days
    price = DecimalField(default=0, max_digits=20, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        verbose_name = "Membership"
        verbose_name_plural = "Memberships"
        ordering = ["-created", "-modified"]


class UserMembership(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="usermembership")
    membership = ForeignKey(
        Membership, on_delete=SET_NULL, null=True, related_name="usermembership"
    )

    def __str__(self):
        return self.user.fullname


class Investor(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="investorprofile")
    recommended_by = ForeignKey(
        User, on_delete=CASCADE, blank=True, null=True, related_name="ref_by"
    )

    def __str__(self):
        return self.user.fullname

    # def save(self, *args, **kwargs):
    #     self.user.is_field_worker = False
    #     self.user.save()
    #     super(Investor, self).save(*args, **kwargs)


    class Meta:
        managed = True
        verbose_name = "Investor"
        verbose_name_plural = "Investors"
        ordering = ["-created", "-modified"]


class FieldWorker(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="fieldworkerprofile")
    is_employed = BooleanField(default=True)
    

    # def save(self, *args, **kwargs):
    #     self.user.is_field_worker = True
    #     self.user.save()
    #     super(FieldWorker, self).save(*args, **kwargs)

    def years_of_service(self):
        if not self.is_employed:
            today = datetime.date.today()
            if self.user.member_since:
                return (
                    "%s" % relativedelta.relativedelta(today, self.user.member_since).years
                )
            else:
                return None

    def get_recommended_users(self):
        qs = Investor.objects.all()
        my_recommended = []
        for user in qs:
            if user.recommended_by == self.user:
                my_recommended.append(user)
        return my_recommended

    # def deactivated(self):
    #     if not self.is_employed:

    def __str__(self):
        return self.user.fullname

    class Meta:
        managed = True
        verbose_name = "FieldWorker"
        verbose_name_plural = "FieldWorkers"
        ordering = ["-created", "-modified"]


class Subscription(TimeStampedModel):
    user_membership = ForeignKey(
        UserMembership, related_name="subscription", on_delete=CASCADE
    )
    active = BooleanField(default=False)

    def __str__(self):
        return self.user.fullname

    class Meta:
        managed = True
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ["-created", "-modified"]
