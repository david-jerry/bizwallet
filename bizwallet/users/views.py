import datetime
import json
from datetime import datetime as dt
from datetime import timedelta

import requests
from allauth.account.forms import SignupForm
from allauth.account.views import SignupView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
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
)
from bizwallet.users.models import (  # Subscribe,
    Membership,
    NextOfKin,
    PayHistory,
    Profile,
    Subscription,
    UserMembership,
    UserSettings,
)
from config import settings

User = get_user_model()

class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        
        if user.is_field_worker:
            recommended_users = user.get_recommended_users()
            context['my_recs'] = recommended_users
        else:
            context['my_recs'] = "Failed to show any"
        
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



def subscription(request):
	return render(request, 'subscription.html')

def end_sub(request):
	return render(request, 'sub.html')


def subscribe(request):
	plan = request.GET.get('sub_plan')
	fetch_membership = Membership.objects.filter(membership_type=plan).exists()
	if fetch_membership == False:
		return HttpResponseRedirect('subscribe')
	membership = Membership.objects.get(membership_type=plan)
	price = float(membership.price)*100 # We need to multiply the price by 100 because Paystack receives in kobo and not naira.
	price = int(price)

	def init_payment(request):
		url = 'https://api.paystack.co/transaction/initialize'
		headers = {
			'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
			'Content-Type' : 'application/json',
			'Accept': 'application/json',
			}
		datum = {
			"email": request.user.email,
			"amount": price
			}
		x = requests.post(url, data=json.dumps(datum), headers=headers)
		if x.status_code != 200:
			return str(x.status_code)
		
		results = x.json()
		return results
	initialized = init_payment(request)
	print(initialized['data']['authorization_url'])
	amount = price/100
	instance = PayHistory.objects.create(amount=amount, payment_for=membership, user=request.user, paystack_charge_id=initialized['data']['reference'], paystack_access_code=initialized['data']['access_code'])
	UserMembership.objects.filter(user=instance.user).update(reference_code=initialized['data']['reference'])
	link = initialized['data']['authorization_url']
	return HttpResponseRedirect(link)
	return render(request, 'users/subscribe.html')



def call_back_url(request):
	reference = request.GET.get('reference')
	# We need to fetch the reference from PAYMENT
	check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
	if check_pay == False:
		# This means payment was not made error should be thrown here...
		print("Error")
	else:
		payment = PayHistory.objects.get(paystack_charge_id=reference)
		# We need to fetch this to verify if the payment was successful.
		def verify_payment(request):
			url = 'https://api.paystack.co/transaction/verify/'+reference
			headers = {
				'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
				'Content-Type' : 'application/json',
				'Accept': 'application/json',
				}
			datum = {
				"reference": payment.paystack_charge_id
				}
			x = requests.get(url, data=json.dumps(datum), headers=headers)
			if x.status_code != 200:
				return str(x.status_code)
			
			results = x.json()
			return results
	initialized = verify_payment(request)
	if initialized['data']['status'] == 'success':

		PayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
		new_payment = PayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
		instance = Membership.objects.get(id=new_payment.payment_for.id)
		sub = UserMembership.objects.filter(reference_code=initialized['data']['reference']).update(membership=instance)
		user_membership = UserMembership.objects.get(reference_code=initialized['data']['reference'])
		Subscription.objects.create(user_membership=user_membership, expires_in=dt.now().date() + timedelta(days=user_membership.membership.duration))
		return redirect('subscribed')
	return render(request, 'payment.html')


def subscribed(request):
	return render(request, 'subscribed.html')


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
