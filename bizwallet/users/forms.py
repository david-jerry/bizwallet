from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import fields
from django.utils.translation import gettext_lazy as _

from .models import EnrollmentPlan, NextOfKin, Profile, Subscribe, Testimonial

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        fields = [
            "username",
            # "first_name",
            # "last_name",
            # "username",
            # "email",
            # "phone_no",
            # "gender",
            # "dob",
            "marital",
            # "phone_no",
            # "state",
            "address",
            # "accept_terms",
        ]


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = [
            "image",
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


class InvestorSignupForm(SignupForm):
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_field_worker = False
        user.save()
        return user


class FieldWorkerSignupForm(SignupForm):
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_field_worker = True
        user.save()
        return user


class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["testimony"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "account_number",
            "bvn",
            "bank_name"
        ]


class KinForm(forms.ModelForm):
    class Meta():
        model = NextOfKin
        fields = [
            'first_name', 
            'middle_name', 
            'last_name', 
            'image', 
            'gender', 
            'dob', 
            'phone_no', 
            'address'
        ]

    # @transaction.atomic
    # def save(self):
    #     kin = super().save(commit=False)
    #     kin.user = self.request.user
    #     kin.save()
    #     return kin



class PlanForm(forms.ModelForm):
    class Meta():
        model = EnrollmentPlan
        fields = [
            'title', 
            "percentage", 
            "invest", 
            'status', 
            'duration'
        ]


class SubscribeForm(forms.ModelForm):
    class Meta():
        model = Subscribe
        fields = ['bill']

    # @transaction.atomic
    # def save(self):
    #     sub = super().save(commit=False)
    #     sub.user = self.request.user
    #     sub.save()
    #     return sub
