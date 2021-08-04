from allauth.account.signals import user_logged_in, user_signed_up
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from bizwallet.utils.send_mass_html_mail import send_mass_html_mail
from bizwallet.utils.unique_slug_generator import unique_slug_generator

from .models import Profile, Subscribe

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        instance.userprofile.save()
















# plan slugfield receiver
# @receiver(pre_save, sender=Plan)
# def create_plan_slug(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)






# send plan registration form
@receiver(post_save, sender=Subscribe)
def post_save_send_email(sender, instance, created, *args, **kwargs):
    user = User.objects.get(username=instance.user.username)
    if created:
        obj = Subscribe.objects.get(user=instance.user)
        obj.send_subscribed_mail()


from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy


@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    if not user.has_paid:
        HttpResponseRedirect(reverse_lazy("users:subscribe"))
        
    user_ip = request.session.get("user_ip")
    # user_country = request.session.get("country")
    # user_country_code = request.session.get("country_code")
    user_city = request.session.get("city")
    user.ip = user_ip
    user.city = user_city
    user.save()


@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
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












