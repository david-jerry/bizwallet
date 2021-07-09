from allauth.account.forms import SignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import FieldWorker, Investor

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        fields = [
            "username"
            # "first_name",
            # "last_name",
            # "username",
            # "email",
            # "phone_no",
            # "gender",
            # "dob",
            # "marital",
            # "phone_no",
            # "state",
            # "address",
            # "accept_terms",
        ]


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_no",
            "gender",
            "dob",
            "marital",
            "phone_no",
            "state",
            "address",
            "accept_terms",
        ]

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


# class InvestorSignupForm(SignupForm):
#     def save(self, request):
#         user = super(InvestorSignupForm, self).save(request)
#         investor_user = Investor(user=user, user_is_field_worker=False)
#         investor_user.save()

#         return investor_user.user


# class FieldWorkerSignupForm(SignupForm):
#     def save(self, request):
#         user = super(FieldWorkerSignupForm, self).save(request)
#         fw_user = FieldWorker(user=user, user_is_field_worker=True)
#         print("is working", fw_user)
#         # user.is_field_worker=True
#         # user.save()
#         fw_user.save()

#         return fw_user.user
