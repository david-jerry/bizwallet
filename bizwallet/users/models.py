from __future__ import absolute_import

# development system imports
import os
import random
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal

# Third partie imports
from countries_plus.models import Country
from dateutil import relativedelta
from django.conf import settings
# django imports
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
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
    PositiveIntegerField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.db.models.fields import BigIntegerField
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField

from bizwallet.core.models import Services

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

def kin_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "user-kin-photo/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


MEMBERSHIP_CHOICES = (
    ("DIAMOND", "diamond"),
    ("GOLD", "gold"),
    ("BRONZE", "bronze"),
    ("FREE", "free"),
)

BANKS = (
    ('', _('SELECT BANK')),
    ('ACCESS BANK PLC', _('ACCESS BANK PLC')),
    ('CITIBANK NIG. PLC', _('CITIBANK NIG. PLC')),
    ('ECOBANK NIG. PLC', _('ECOBANK NIG. PLC')),
    ('FIDELITY BANK PLC', _('FIDELITY BANK PLC')),
    ('FIRST BANK NIG. LTD', _('FIRST BANK NIG. LTD')),
    ('FIRST CITY MONUMENT BANK PLC', _('FIRST CITY MONUMENT BANK PLC')),
    ('GLOBUS BANK LTD', _('GLOBUS BANK LTD')),
    ('GUARANTY TRUST BANK PLC', _('GUARANTY TRUST BANK PLC')),
    ('HERITAGE BANKING COMPANY LTD', _('HERITAGE BANKING COMPANY LTD')),
    ('KEYSTONE BANK', _('KEYSTONE BANK')),
    ('POLARIS BANK', _('POLARIS BANK')),
    ('PROVIDUS BANK', _('PROVIDUS BANK')),
    ('STANBIC IBTC BANK LTD', _('STANBIC IBTC BANK LTD')),
    ('STANDARD CHARTERED BANK NIG. LTD', _('STANDARD CHARTERED BANK NIG. LTD')),
    ('STERLING BANK PLC', _('STERLING BANK PLC')),
    ('SUNTRUST BANK NIG. PLC', _('SUNTRUST BANK NIG. PLC')),
    ('TITAN TRUST BANK LTD', _('TITAN TRUST BANK LTD')),
    ('UNION BANK OF NIG. PLC', _('UNION BANK OF NIG. PLC')),
    ('UNITED BANK FOR AFRICA PLC', _('UNITED BANK FOR AFRICA PLC')),
    ('UNITY BANK PLC', _('UNITY BANK PLC')),
    ('WEMA BANK PLC', _('WEMA BANK PLC')),
    ('ZENITH BANK PLC', _('ZENITH BANK PLC')),
)


class User(AbstractUser):
    """Default user for bizwallet."""

    middle_name = CharField(_("Middle Name"), max_length=255, blank=True, null=True)
    balance = DecimalField(
        default=0, max_digits=20, decimal_places=2, blank=True, null=True
    )
    ip = GenericIPAddressField(
        _("User IP"), protocol="both", unpack_ipv4=False, blank=True, null=True
    )
    image = ResizedImageField(size=[300, 300], quality=75, crop=['middle', 'center'], upload_to=profile_image, force_format='JPEG')
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
    company = CharField(_("Company Name"), max_length=500, blank=True, null=True)
    occupation = CharField(_("Occupation"), max_length=500, blank=True, null=True)
    office_address = CharField(_("Office Address"), max_length=500, blank=True, null=True)
    is_field_worker = BooleanField(_("Are you a field worker"), default=True)
    accept_terms = BooleanField(_("Accept our terms"), default=False)
    has_paid = BooleanField(_("Paid Initial Membership Fee"), default=False)

    
    # Referral fields
    recommended_by = ForeignKey(
        "self", on_delete=CASCADE, blank=True, null=True, related_name="ref_by"
    )



    def get_recommended_users(self):
        qs = User.objects.all()
        my_recommended = []
        for user in qs:
            if user.recommended_by == self:
                my_recommended.append(user)
        return my_recommended

   
    # user initials
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



class UserSettings(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name='usersettings')
    account_verified = BooleanField(default=False)
    ver_expired = DateField(default=datetime.now().date() + timedelta(days=3))
    verified_code = CharField(blank=True, null=True, max_length=100)
    code_expired = BooleanField(default=False)
    recieve_email_notice = BooleanField(default=True)

class PayHistory(TimeStampedModel):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    paystack_charge_id = CharField(max_length=100, default='', blank=True)
    paystack_access_code = CharField(max_length=100, default='', blank=True)
    payment_for = ForeignKey('Membership', on_delete=SET_NULL, null=True)
    amount = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = BooleanField(default=False)
    date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.fullname


class LoginHistory(TimeStampedModel):
    user = ForeignKey(User, on_delete=CASCADE, related_name='loginhistory')

    def __str__(self):
        return f"{self.user.fullname} logged in {self.created}"
    

class Membership(TimeStampedModel):
    MEMBERSHIP_CHOICES = (
    	('Premium', 'Premium'), # Note that they are all capitalize//
    	('Platinum', 'Platinum'),
    	('Gold', 'Gold'),
        ('VIP', 'VIP'),
        ('VVIP', 'VVIP')
    )
    PERIOD_DURATION = (
        ('Days', 'Days'),
        ('Week', 'Week'),
        ('Months', 'Months'),
    )
    slug = SlugField(null=True, blank=True)
    membership_type = CharField(choices=MEMBERSHIP_CHOICES, default='Premium', max_length=30)
    duration = PositiveIntegerField(default=365)
    duration_period = CharField(max_length=100, default='Days', choices=PERIOD_DURATION)
    price = DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
       return self.membership_type

class UserMembership(TimeStampedModel):
    user = OneToOneField(User, related_name='user_membership', on_delete=CASCADE)
    membership = ForeignKey(Membership, related_name='user_membership', on_delete=SET_NULL, null=True)
    reference_code = CharField(max_length=100, default='', blank=True)

    def __str__(self):
       return self.user.fullname



#### User Subscription
class Subscription(TimeStampedModel):
    user_membership = ForeignKey(UserMembership, related_name='subscription', on_delete=CASCADE, default=None)
    expires_in = DateField(null=True, blank=True)
    active = BooleanField(default=True)

    def __str__(self):
      return self.user_membership.user.fullname

    def has_paid(self):
        if self.active:
            user = self.user_membership.user
            user.has_paid = True
            user.save()
        else:
            user = self.user_membership.user
            user.has_paid = False
            user.save()

    def send_subscribed_mail(self):
        user = self.user_membership.user
        plan = self.user_membership.membership

        if self.active:
            html_ = render_to_string("email/subscribe_approve.html", {"fullname": f"{user.fullname}", "user_plan": f"{plan.membership_type}"})
            subject = "Subscription Plan Started Successfully"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient = [user.email]
            sent_mail = send_mail(
                subject,
                "Your subscription has been activated and started",
                from_email,
                recipient,
                html_message=html_,
                fail_silently=False
            )
            return sent_mail
        return False


class Profile(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="userprofile")
    account_number = BigIntegerField(_("Account Number"), unique=True, null=True, blank=True)
    bvn = CharField(_("Bank Verification Number (BVN)"), max_length=255, null=True, blank=False, unique=True)
    bank_name = CharField(_("Bank Name"), max_length=255, choices=BANKS, null=True, blank=False,)

    @property
    def years_of_service(self):
        if self.user.is_field_worker and self.user.member_since:
            today = datetime.date.today()
            return ("%s" % relativedelta.relativedelta(today, self.user.member_since).years)


    def __str__(self):
        return self.user.fullname

    class Meta:
        managed = True
        verbose_name = "FieldWorker"
        verbose_name_plural = "FieldWorkers"
        ordering = ["-created", "-modified"]





class NextOfKin(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="nextofkin")

    first_name = CharField(_("First Name"), max_length=255, blank=True, null=True)
    middle_name = CharField(_("Middle Name"), max_length=255, blank=True, null=True)
    last_name = CharField(_("Last Name"), max_length=255, blank=True, null=True)
    image = ResizedImageField(size=[300, 300], quality=75, crop=['middle', 'center'], upload_to=kin_image, force_format='JPEG')
    gender = CharField(_("Gender"), max_length=7, blank=True, null=True, choices=SEX)
    dob = DateField(_("Date of Birth"), blank=True, null=True)
    phone_no = CharField(_("Phone Number"), blank=True, null=True, max_length=13, unique=True)
    address = CharField(
        _("Residntial Address"), max_length=600, null=True, blank=True
    )

    @property
    def kin(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.kin} is a kin to {self.user.fullname}"

    class Meta:
        managed = True
        verbose_name = "Kin"
        verbose_name_plural = "Kins"
        ordering = ["-created", "-modified"]



class Testimonial(TimeStampedModel):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, related_name="usertestimonial")
    testimony = CharField(_("Testimony"), max_length=400, blank=True, null=True)
    active = BooleanField(default=False)
    
    def __str__(self):
        return self.user.fullname

    class Meta:
        managed = True
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = [ "-created", "-modified"]
















































# class EnrollmentPlan(TimeStampedModel):
#     DURATION = (
#         ("0", "0"),
#         ("28", "28"),
#         ("64", "64"),
#         ("112", "112"),
#         ("168", "168"),
#         ("336", "336"),
#         ("672", "672")
#     )
#     STATUS = Choices("pending", "approved", "rejected", "expired")
#     title = CharField(_('Enrollment Plan Title'), max_length=255, null=True, blank=True)
#     percentage = DecimalField(_("Plan Percentage"), max_digits=3, decimal_places=2, null=True, blank=True, default=1.0, help_text="1.00 means 100%, 0.50 mean 50%")
#     slug = SlugField(_('Plan Slug'), max_length=500, unique=True, null=True, blank=True)
#     duration = CharField(_("Duration"), max_length=4, choices=DURATION, null=True, blank=True, default="168")
#     invest = DecimalField(
#         _("Minimum & Maximum Investment Amount"), decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('50000.00')), MaxValueValidator(Decimal('2000000.00'))], help_text="min-amount: ₦50,000.00, max-amount: ₦2,000,000.00", null=True, blank=True
#     )
#     status = StatusField(default="pending")

#     def __str__(self):
#         return self.title

#     class Meta:
#         managed = True
#         verbose_name = "Plan"
#         verbose_name_plural = "Plans"
#         ordering = ["-created", "-modified"]


# class Subscribe(TimeStampedModel):
#     user = OneToOneField(User, on_delete=SET_NULL, null=True, blank=True)
#     plan = ForeignKey(EnrollmentPlan, on_delete=SET_NULL, null=True, blank=True, related_name="userplan")
#     bill = DecimalField(
#         _("Minimum & Maximum Investment Amount"), decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('50000.00')), MaxValueValidator(Decimal('2000000.00'))], help_text="min-amount: ₦50,000.00, max-amount: ₦2,000,000.00", null=True, blank=True
#     )
#     started_on = DateTimeField(_("Plan Started on"), auto_now=True)
#     approved = BooleanField(default=False)

#     def __str__(self):
#         return f"{self.user.fullname} subscribed for {self.plan.title} with {self.bill} for over {self.plan.duration} days"


#     # check if user has paid for a subscription
#     def subscribed(self):
#         # qs = User.objects.filter(user=self.user, has_paid=False)
#         if self.approved:
#             user = self.user
#             user.has_paid = True
#             self.started_on = timezone.now()
#             user.save()
#             self.save()
#             return True
#         return False

#     def send_subscribed_mail(self):
#         if self.subscribed:
#             html_ = render_to_string("email/subscribe_approve.html", {"fullname": f"{self.user.fullname}", "user_plan": f"{self.plan}"})
#             subject = "1-Time Subscription Plan Started Successfully"
#             from_email = settings.DEFAULT_FROM_EMAIL
#             recipient = [self.user.email]
#             sent_mail = send_mail(
#                 subject,
#                 "Your subscription has been approved and started",
#                 from_email,
#                 recipient,
#                 html_message=html_,
#                 fail_silently=False
#             )
#             return sent_mail
#         return False


#     class Meta:
#         managed = True
#         verbose_name = "Subscribe"
#         verbose_name_plural = "Subscriptions"
#         ordering = ["-created", "-modified"]



