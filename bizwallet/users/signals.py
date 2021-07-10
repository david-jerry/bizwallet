from allauth.account.signals import user_logged_in, user_signed_up
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FieldWorker, Investor

User = get_user_model()


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     print("****", created)
#     if instance.is_field_worker == False:
#         FieldWorker.objects.get_or_create(user=instance)
#     else:
#         Investor.objects.get_or_create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     print("_-----")
#     # print(instance.internprofile.bio, instance.internprofile.location)
#     if instance.is_field_worker:
#         instance.fieldworkerprofile.save()
#     else:
#         Investor.objects.get_or_create(user=instance)

@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    user_ip = request.session.get("user_ip")
    user_country = request.session.get("country")
    user_country_code = request.session.get("country_code")
    user_city = request.session.get("city")
    user.ip = user_ip
    user.city = user_city
    print("___login____", user.is_field_worker)
    user.save()



@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    # print("****", user)
    user_ip = request.session.get("user_ip")
    user_country = request.session.get("country")
    user_country_code = request.session.get("country_code")
    user_city = request.session.get("city")
    referrer_id = request.session.get("fieldworker_id")
    if referrer_id is not None:
        new_investor = Investor.objects.get(user_id=user.id)
        print("-----", new_investor)
        recommender = FieldWorker.objects.get(user_id=referrer_id)
        print("-----referal", recommender)
        recommender_email = recommender.user.email
        new_investor.user.country = str(user_country)
        new_investor.user.city = user_city
        new_investor.user.ip = user_ip
        new_investor.recommended_by = recommender
        new_investor.user.save()
        messages.success(request, "REFERRAL REGISTRATION WAS SUCCESSFUL")
        email = (
            (
                "NEW REFERRAL REGISTRATION Bizwallet NG",
                f"{user.fullname} just registered with this email \n Email: {user.email}",
                "noreply@bizwallet.org",
                ["admin@bizwallet.org"],
            ),
            (
                "NEW REFERAL LINK REGISTRATION Bizwallet NG",
                f"{user.fullname} just registered with this email \n Email: {user.email}",
                "noreply@bizwallet.org",
                [recommender_email],
            ),
        )
        send_mass_mail(email, fail_silently=False)
    elif referrer_id is None:
        if request.path == "/accounts/signup-fieldworker/" and not request.path == "/accounts/signup/":
            recommender = FieldWorker.objects.create(user_id=user.id)
            recommender.user.country = user_country_code
            recommender.user.city = user_city
            recommender.user.ip = user_ip
            recommender.user.is_field_worker=True
            recommender.user.save()
            messages.success(request, "FIELDWORKER REGISTRATION WAS SUCCESSFUL")
            send_mail(
                "NEW FIELDWORKER REGISTRATION Bizwallet NG",
                f"{recommender.user.fullname} just registered with this email \n Email: {user.email}",
                "noreply@bizwallet.org",
                ["admin@bizwallet.org"],
                fail_silently=False,
            )
        elif request.path == "/accounts/signup/" and not request.path == "/accounts/signup-fieldworker/":
            new_investor = Investor.objects.create(user_id=user.id)
            new_investor.user.country = user_country_code
            new_investor.user.city = user_city
            new_investor.user.is_field_worker=False
            new_investor.user.ip = user_ip
            new_investor.user.save()
            messages.success(request, "INVESTOR REGISTRATION WAS SUCCESSFUL")
            send_mail(
                "NEW INVESTOR REGISTRATION Bizwallet NG",
                f"{new_investor.user.fullname} just registered with this email \n Email: {user.email}",
                "noreply@bizwallet.org",
                ["admin@bizwallet.org"],
                fail_silently=False,
            )
