from datetime import datetime

from allauth.account.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
    user_signed_up,
)
from django.contrib import messages
from django.contrib.auth import get_user_model
# from django.contrib.auth.signals import (
#     user_logged_in,
#     user_logged_out,
#     user_login_failed,
# )
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from bizwallet.users.models import (
    BalHistory,
    LoginHistory,
    Membership,
    Subscription,
    UserMembership,
)
from bizwallet.utils.send_mass_html_mail import send_mass_html_mail
from bizwallet.utils.unique_slug_generator import unique_slug_generator

from .models import Membership, Profile, Subscribe, UserSettings

User = get_user_model()

today = datetime.date.today()




# user signals

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

# @receiver(post_save, sender=User)
# def balance_history(sender, instance, created, *args, **kwargs):
#     if instance:
#         BalHistory.objects.create(user=instance, amount=instance.balance)






















# Subscription signals for payments

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
                "noreply@bizwallet.org",
                ["admin@bizwallet.org", recommender_email],
                html_message=html_message,
                fail_silently=False,
            )
        elif referrer_id is None:
            user.country = user_country_code
            user.city = user_city
            user.ip = user_ip
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
                "noreply@bizwallet.org",
                ["admin@bizwallet.org"],
                html_message=html_message,
                fail_silently=False,
            )












