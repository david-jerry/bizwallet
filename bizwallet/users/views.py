import datetime
import json
from datetime import datetime as dt
from datetime import timedelta
from decimal import Decimal

import requests
from allauth.account.forms import SignupForm
from allauth.account.views import SignupView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Avg, Count, F, Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)

from bizwallet.users.forms import (  # SubscribeForm,
    FieldWorkerSignupForm,
    InvestorSignupForm,
    KinForm,
    WithdrawalForm,
)
from bizwallet.users.models import (  # Subscribe,
    BalHistory,
    LoginHistory,
    Membership,
    NextOfKin,
    PayHistory,
    Profile,
    Subscription,
    UserMembership,
    UserSettings,
    Withdrawals,
)
from bizwallet.utils.bal_chart import get_year_dict, months

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        # else:
        #     context["my_recs"] = "Failed to show any"
        #     context["refs_count"] = 0

        current_year = dt.now().strftime("%Y")
        current_syear = dt.now().strftime("%y")
        previous_year = int(current_year) - 1
        previous_syear = int(current_syear) - 1

        context["c_year"] = current_year
        context["c_syear"] = current_syear
        context["p_year"] = previous_year
        context["p_syear"] = previous_syear

        balances = (
            BalHistory.objects.filter(date__year=current_year, user=self.request.user)
            .annotate(price=F("amount"))
            .values("price")
            .annotate(month=ExtractMonth("date"))
            .values("month")
            .annotate(average=Sum("amount"))
            .values("average")
            .order_by("month")
        )
        prev_balances = (
            BalHistory.objects.filter(date__year=previous_year, user=self.request.user)
            .annotate(price=F("amount"))
            .values("price")
            .annotate(month=ExtractMonth("date"))
            .values("month")
            .annotate(average=Sum("amount"))
            .values("average")
            .order_by("month")
        )

        context["c_bal"] = balances
        context["p_bal"] = prev_balances

        if user.is_field_worker:
            recommended_users = user.get_recommended_users()
            context["my_recs"] = recommended_users
            context["refs_count"] = len(recommended_users)

        withdrawals = Withdrawals.objects.filter(user__user=self.request.user).aggregate(Sum('amount'))['amount__sum']
        if not withdrawals:
            withdrawals_default = 0.00
            context["withdrwals"] = withdrawals_default
            prf_perc = ((Decimal(self.request.user.balance) - Decimal(withdrawals_default)) / Decimal(self.request.user.balance)) * 100
            context["prf_perc"] = prf_perc
        else:
            context["withdrwals"] = withdrawals
        # months = months
            prf_perc = (Sum(self.request.user.balance) - withdrawals) / Sum(self.request.user.balance)
            context["prf_perc"] = prf_perc


        p_history = PayHistory.objects.all().filter(user=self.request.user)[:10]
        context['p_his'] = p_history

        l_history = LoginHistory.objects.all().filter(user=self.request.user)[:10]
        context['l_his'] = l_history
        return context


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["first_name", "last_name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_field_worker:
            recommended_users = user.get_recommended_users()
            context["my_recs"] = recommended_users
            context["refs_count"] = len(recommended_users)

        withdrawals = Withdrawals.objects.filter(user__user=self.request.user).aggregate(Sum('amount'))['amount__sum']
        if not withdrawals:
            withdrawals_default = 0.00
            context["withdrwals"] = withdrawals_default
            prf_perc = ((Decimal(self.request.user.balance) - Decimal(withdrawals_default)) / Decimal(self.request.user.balance)) * 100
            context["prf_perc"] = prf_perc
        else:
            context["withdrwals"] = withdrawals
        # months = months
            prf_perc = (Sum(self.request.user.balance) - withdrawals) / Sum(self.request.user.balance)
            context["prf_perc"] = prf_perc

        return context


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class InvestorSignupView(SignupView):
    template_name = "account/signup_investor.html"
    success_url = reverse_lazy("account_login")
    form_class = InvestorSignupForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["user"] = self.object
    #     return context

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     images = context['images']
    #     with transaction.atomic():
    #         form.instance.dealer = self.request.user
    #         form.instance.car_dealer_name = self.request.user.full_name
    #         form.instance.car_dealer_phone = self.request.user.phone_no
    #         self.object = form.instance.save()
    #         if images.is_valid():
    #             images.instance.car = self.object
    #             images.instance.save()
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('cars:detail', kwargs={'slug':self.object.slug})


investor_signup = InvestorSignupView.as_view()


class FieldWorkerSignupView(SignupView):
    template_name = "account/signup_fieldworker.html"
    success_url = reverse_lazy("account_login")
    form_class = FieldWorkerSignupForm


fieldworker_signup = FieldWorkerSignupView.as_view()


@login_required
def subscription(request):
    return render(request, "users/subscription.html")


@login_required
def end_sub(request):
    return render(request, "sub.html")


class WithdrawalView(LoginRequiredMixin, CreateView):
    model = Withdrawals
    template_name = "users/withdraw.html"
    form_class = WithdrawalForm

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_field_worker:
            recommended_users = user.get_recommended_users()
            context["my_recs"] = recommended_users
            context["refs_count"] = len(recommended_users)

        withdrawals = Withdrawals.objects.filter(user__user=self.request.user).aggregate(Sum('amount'))['amount__sum']
        if not withdrawals:
            withdrawals_default = 0.00
            context["withdrwals"] = withdrawals_default
            prf_perc = ((Decimal(self.request.user.balance) - Decimal(withdrawals_default)) / Decimal(self.request.user.balance)) * 100
            context["prf_perc"] = prf_perc
        else:
            context["withdrwals"] = withdrawals
        # months = months
            prf_perc = (Sum(self.request.user.balance) - withdrawals) / Sum(self.request.user.balance)
            context["prf_perc"] = prf_perc

        return context

    def form_valid(self, form):
        form.instance.user.user = self.request.user
        user = form.instance.user.user
        amount = form.instance.amount

        # def init_payment(request):
        #     url = "https://api.paystack.co/transferrecipient"
        #     headers = {
        #         "Authorization": "Bearer " + settings.PAYSTACK_SECRET_KEY,
        #         "Content-Type": "application/json",
        #         "Accept": "application/json",
        #     }
        #     datum = {
        #         "type": "nuban",
        #         "name": self.request.user.fullname,
        #         "description": f"Wallet withdrawals for personal use",
        #         "account_number": self.request.user.userprofile.account_name,
        #         "amount": (amount * 100),
        #     }
        #     x = requests.post(url, data=json.dumps(datum), headers=headers)
        #     if x.status_code != 200:
        #         return str(x.status_code)

        #     results = x.json()
        #     return results

        # initialized = init_payment(self.request)
        # amount = price / 100

        if amount < user.balance:
            balance = user.balance - amount
            User.objects.filter(username=user.username).update(balance=balance, wd_status="Pending")
            messages.success(self.request, "Withdrawal Request made")
        elif amount > user.balance:
            messages.warning(self.request, "Insufficient Balance")
        return super().form_valid(form)


@login_required
def subscribe(request):
    plan = request.GET.get("sub_plan")
    fetch_membership = Membership.objects.filter(membership_type=plan).exists()
    if fetch_membership == False:
        messages.info(request, "You have no subscription plan")
        return redirect(reverse_lazy("users:subscribe"))
    membership = Membership.objects.get(membership_type=plan)
    price = (
        float(membership.price) * 100
    )  # We need to multiply the price by 100 because Paystack receives in kobo and not naira.
    price = int(price)

    def init_payment(request):
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": "Bearer " + settings.PAYSTACK_SECRET_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        datum = {"email": request.user.email, "amount": price}
        x = requests.post(url, data=json.dumps(datum), headers=headers)
        if x.status_code != 200:
            return str(x.status_code)

        results = x.json()
        return results

    initialized = init_payment(request)
    amount = price / 100
    instance = PayHistory.objects.create(
        amount=amount,
        payment_for=membership,
        user=request.user,
        paystack_charge_id=initialized["data"]["reference"],
        paystack_access_code=initialized["data"]["access_code"],
    )
    BalHistory.objects.create(user=request.user, amount=instance.amount)
    UserMembership.objects.filter(user=instance.user).update(
        reference_code=initialized["data"]["reference"]
    )
    balance = request.user.balance + Decimal(instance.amount)
    User.objects.filter(username=instance.user.username).update(
        has_paid=True, balance=balance
    )
    link = initialized["data"]["authorization_url"]
    messages.success(request, f"Finalizing payments for {plan} plan")
    return HttpResponseRedirect(link)
    return render(request, "users/subscribe.html")


def call_back_url(request):
    reference = request.GET.get("reference")
    # We need to fetch the reference from PAYMENT
    check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
    if check_pay == False:
        # This means payment was not made error should be thrown here...
        print("Error")
    else:
        payment = PayHistory.objects.get(paystack_charge_id=reference)
        # We need to fetch this to verify if the payment was successful.
        def verify_payment(request):
            url = "https://api.paystack.co/transaction/verify/" + reference
            headers = {
                "Authorization": "Bearer " + settings.PAYSTACK_SECRET_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            datum = {
                # "user": request.user.fullname,
                # "email": request.user.email,
                "reference": payment.paystack_charge_id
            }
            x = requests.get(url, data=json.dumps(datum), headers=headers)
            if x.status_code != 200:
                return str(x.status_code)

            results = x.json()
            return results

    initialized = verify_payment(request)
    if initialized["data"]["status"] == "success":
        PayHistory.objects.filter(
            paystack_charge_id=initialized["data"]["reference"]
        ).update(paid=True)
        new_payment = PayHistory.objects.get(
            paystack_charge_id=initialized["data"]["reference"]
        )
        instance = Membership.objects.get(id=new_payment.payment_for.id)
        sub = UserMembership.objects.filter(
            reference_code=initialized["data"]["reference"]
        ).update(membership=instance)
        user_membership = UserMembership.objects.get(
            reference_code=initialized["data"]["reference"]
        )
        Subscription.objects.create(
            user_membership=user_membership,
            expires_in=dt.now().date()
            + timedelta(days=user_membership.membership.duration),
        )
        messages.success(
            request,
            f"You have successfully subscribed for {instance.membership_type} plan",
        )
        return redirect("users:detail", request.user.username)
    return render(request, "payment.html")


class KinCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = NextOfKin
    template_name = "users/kin.html"
    form_class = KinForm
    success_message = _("Successfully Added a next of Kin to Bizwallet Co-Operative")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_field_worker:
            recommended_users = user.get_recommended_users()
            context["my_recs"] = recommended_users
            context["refs_count"] = len(recommended_users)

        withdrawals = Withdrawals.objects.filter(user__user=self.request.user).aggregate(Sum('amount'))['amount__sum']
        if not withdrawals:
            withdrawals_default = 0.00
            context["withdrwals"] = withdrawals_default
            prf_perc = ((Decimal(self.request.user.balance) - Decimal(withdrawals_default)) / Decimal(self.request.user.balance)) * 100
            context["prf_perc"] = prf_perc
        else:
            context["withdrwals"] = withdrawals
        # months = months
            prf_perc = (Sum(self.request.user.balance) - withdrawals) / Sum(self.request.user.balance)
            context["prf_perc"] = prf_perc

        return context

kin_creation = KinCreateView.as_view()


# class SubscribeView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Subscription
#     template_name = "users/subscribe.html"
#     fields = ['']
#     success_message = _("Successfully Subscribed to Bizwallet Co-Operative")

#     def get_success_url(self):
#         return self.request.user.get_absolute_url()  # type: ignore [union-attr]

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.instance.save()
#         return super().form_valid(form)

# subscribe_view = SubscribeView.as_view()
