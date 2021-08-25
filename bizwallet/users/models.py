from __future__ import absolute_import

# development system imports
import os
import random
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal

from allauth.account.signals import user_logged_in, user_logged_out, user_signed_up
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
    IntegerField,
    ManyToManyField,
    OneToOneField,
    PositiveIntegerField,
    SlugField,
    TextChoices,
    TextField,
    URLField,
    UUIDField,
)
from django.db.models.fields import BigIntegerField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
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

def plan_image(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "plan-cover-photo/{new_filename}/{final_filename}".format(
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


class Banks(TimeStampedModel):
    title = CharField(_('Bank Name'), null=True, blank=True, max_length=500, unique=True)
    country = CharField(_('Bank Country'), null=True, blank=True, max_length=500)
    currency = CharField(_('Bank currency'), null=True, blank=True, max_length=3)
    slug = SlugField(max_length=700, blank=True, null=True, unique=True)
    bank_code = CharField(_('Bank Code'), max_length=5, blank=True, null=True, unique=False)
    bank_id = CharField(_('Bank ID'), max_length=5, blank=True, null=True)

    def __str__(self):
        return self.title

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
    has_testified = BooleanField(_("User has testified"), default=False)
    is_verified = BooleanField(_('User is Verified'), default=False)

    
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
        TODAY = datetime.today()
        if self.dob:
            return "%s" % relativedelta.relativedelta(TODAY, self.dob).years
        else:
            return None

    @property
    def fullname(self):
        if self.first_name and self.last_name and self.middle_name:
            fullname = f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            fullname = f"{self.username}"
        return fullname


    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        UserSettings.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        instance.userprofile.save()
        instance.usersettings.save()


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    print('user {} logged out through page {}'.format(user.username, request.META.get('HTTP_REFERER')))

@receiver(user_logged_in)
def login_user_ip(request, sender, user, **kwargs):
    print("Login signal working fine")
    if user:
        ip = request.session.get("user_ip")
        country = request.session.get("country")
        print(country)
        country_code = request.session.get("country_code")
        city = request.session.get("city")
        User.objects.filter(username=user.username).update(country=country, city=city)
        LoginHistory.objects.create(user=user, ip=ip, city=city, country=country)

class Profile(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="userprofile")
    account_number = CharField(_("Account Number"), max_length=10, unique=True, null=True, blank=True)
    bvn = CharField(_("Bank Verification Number (BVN)"), max_length=255, null=True, blank=True, unique=True)
    bank_name = ForeignKey(Banks, on_delete=SET_NULL, related_name="userbank", null=True)
    blacklisted = BooleanField(default=False)

    @property
    def years_of_service(self):
        if self.user.is_field_worker and self.user.member_since:
            today = datetime.date.today()
            return ("%s" % relativedelta.relativedelta(today, self.user.member_since).years)


    def __str__(self):
        return self.user.fullname

    class Meta:
        managed = True
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ["-created", "-modified"]

class UserSettings(TimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name='usersettings')
    account_verified = BooleanField(default=False)
    ver_expired = DateField(default=datetime.now().date() + timedelta(days=3))
    verified_code = CharField(blank=True, null=True, max_length=100)
    code_expired = BooleanField(default=False)
    recieve_email_notice = BooleanField(default=True)

    def title(self):
        return f"{self.user.fullname}"

class PayHistory(TimeStampedModel):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, related_name="user_pay_history")
    paystack_charge_id = CharField(max_length=100, default='', blank=True)
    paystack_access_code = CharField(max_length=100, default='', blank=True)
    payment_for = ForeignKey('Membership', on_delete=SET_NULL, null=True)
    amount = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = BooleanField(default=False)
    date = DateTimeField(auto_now_add=True)


    def title(self):
        return f"{self.user.fullname}"

    def __str__(self):
        return self.user.fullname

class BalHistory(TimeStampedModel):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, default=1)
    date = DateField(auto_now_add=True)
    amount = DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.fullname

class LoginHistory(TimeStampedModel):
    user = ForeignKey(User, on_delete=CASCADE, related_name='loginhistory')
    ip = GenericIPAddressField(
        _("User IP"), protocol="both", unpack_ipv4=False, blank=True, null=True
    )
    country = CharField(_("User Country"), blank=False, null=True, max_length=50)
    city = CharField(_("Located City"), max_length=50, null=True, blank=True)

    def title(self):
        return f"{self.user.fullname}"

    def __str__(self):
        return f"{self.user.fullname} logged in {self.created}"
    


class MembershipFeature(TimeStampedModel):
    title = CharField(_('Membership Feature'), max_length=500, null=True, blank=False)

    def __str__(self):
        return self.title
class Membership(TimeStampedModel):
    MEMBERSHIP_CHOICES = (
    	('Free', 'Free'), # Note that they are all capitalize//
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
    image = ResizedImageField(size=[2287, 1127], quality=75, crop=['middle', 'center'], upload_to=plan_image, force_format='JPEG', null=True)
    membership_type = CharField(choices=MEMBERSHIP_CHOICES, default='Premium', max_length=30)
    features = ManyToManyField(MembershipFeature)
    duration = PositiveIntegerField(default=365)
    duration_period = CharField(max_length=100, default='Days', choices=PERIOD_DURATION)
    price = DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def title(self):
        return f"{self.membership_type}"

    def __str__(self):
       return self.membership_type

class UserMembership(TimeStampedModel):
    user = OneToOneField(User, related_name='user_membership', on_delete=CASCADE)
    membership = ForeignKey(Membership, related_name='user_membership', on_delete=SET_NULL, null=True)
    reference_code = CharField(max_length=100, default='', blank=True)

    def title(self):
        return f"{self.user.fullname}"

    def __str__(self):
       return self.user.fullname


class TopWallet(TimeStampedModel):
    user = ForeignKey(Profile, related_name="user_topup", on_delete=SET_NULL, null=True)
    amount = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference_code = CharField(max_length=100, default='', blank=True)
    access_code = CharField(max_length=100, default='', blank=True)
    paid = BooleanField(default=False)

    def __str__(self):
        return self.user.user.fullname + " added: " + self.amount    

class Withdrawals(TimeStampedModel):
    STATUS = (
        ("Pending", "Pending"),
        ("Complete", "Complete"),
        ("Failed", "Failed")
    )
    user = ForeignKey(Profile, related_name="user_withdrawals", on_delete=SET_NULL, null=True)
    amount = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wd_status = CharField(max_length=100, default='Pending', null=True, choices=STATUS, blank=True)

    def __str__(self):
        return self.user.user.fullname + " withdrew: " + self.amount    

#### User Subscription
class Subscription(TimeStampedModel):
    user_membership = ForeignKey(UserMembership, related_name='subscription', on_delete=CASCADE, default=None)
    expires_in = DateField(null=True, blank=True)
    active = BooleanField(default=True)

    def __str__(self):
      return self.user_membership.user.fullname


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



@receiver(post_save, sender=Testimonial)
def user_testified(sender, created, instance, *args, **kwargs):
    if instance.active:
        User.objects.filter(username=instance.user.username).update(has_testified=True)













































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






@receiver(pre_save, sender=Membership)
def create_post_slug(sender, instance, *args, **kwargs):
	if instance.title and not instance.slug:
		instance.slug = unique_slug_generator(instance)



@receiver(post_save, sender=UserMembership)
def create_subscription(sender, instance, *args, **kwargs):
	if instance:
		Subscription.objects.create(user_membership=instance, expires_in=datetime.now().date() + timedelta(days=instance.membership.duration))



@receiver(post_save, sender=Subscription)
def update_active(sender, created, instance, *args, **kwargs):
    username = instance.user_membership.user.username
    userbal = instance.user_membership.user.balance
    if instance.expires_in < today:
        User.objects.filter(username=username).update(has_paid=False)
        subscription = Subscription.objects.get(id=instance.id)
        subscription.delete()

    # if created and instance.active:
    #     balance = userbal + instance.user_membership.membership.price
    #     User.objects.filter(username=username).update(has_paid=True, balance=balance)

















# All auth signals


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    if user:
        user_ip = request.session.get("user_ip")
        user_country = request.session.get("country")
        user_country_code = request.session.get("country_code")
        user_city = request.session.get("city")
        referrer_id = request.session.get("fieldworker_id")
        if referrer_id is not None:
            new_investor = user
            recommender = User.objects.get(id=referrer_id)
            recommender_email = recommender.email
            new_investor.country = user_country_code
            new_investor.city = user_city
            new_investor.ip = user_ip
            new_investor.balance = Decimal(0.00)
            new_investor.recommended_by = recommender
            new_investor.save()
            get_membership = Membership.objects.get(membership_type="Free")
            membership.instance = UserMembership.objects.create(user=user, membership=get_membership)
            messages.success(request, "REFERRAL REGISTRATION WAS SUCCESSFUL")
            text_email = (
                f"{user.fullname} just registered with this email \n Email: {user.email}"
            )
            html_message = render_to_string(
                "email/new_register.html",
                {"fullname": f"{user.fullname}", "user_mail": f"{user.email}"},
                request=request
            )
            send_mail(
                "NEW REFERRAL REGISTRATION Bizwallet NG",
                text_email,
                "no-reply@bizwallet.org",
                ["admin@bizwallet.org", recommender_email],
                html_message=html_message,
                fail_silently=False,
            )
        elif referrer_id is None:
            user.country = user_country_code
            user.city = user_city
            user.ip = user_ip
            user.balance = Decimal(0.00)
            user.save()
            get_membership = Membership.objects.get(membership_type="Free")
            membership.instance = UserMembership.objects.create(user=user, membership=get_membership)
            messages.success(request, "USER REGISTRATION WAS SUCCESSFUL")
            text_email = f"{user.fullname} just registered with this email \n Email: {user.email}"
            html_message = render_to_string(
                "email/new_register.html",
                {
                    "fullname": f"{user.fullname}",
                    "user_mail": f"{user.email}",
                },
            )
            send_mail(
                "NEW USER REGISTRATION Bizwallet NG",
                text_email,
                "no-reply@bizwallet.org",
                ["admin@bizwallet.org"],
                html_message=html_message,
                fail_silently=False,
            )
