from __future__ import absolute_import

import json
import os

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail, send_mass_mail
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from tinymce.views import render_to_image_list
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from .models import Services
from .forms import ContactForm
from django.template.loader import render_to_string


User = get_user_model()

devnull = open(os.devnull, "w")


def compress_whitespace(s):
    return " ".join(s.split())


@cache_page(1)  # cached in 1 second.. for 15 minutes (60 sec x 15mins)
def home(request, *args, **kwargs):
    # get referrer linked to reffered using username
    username = str(kwargs.get("username"))

    ip_address = request.META.get("HTTP_X_FORWARDED_FOR", "REMOTE_ADDR")
    services = Services.objects.all().filter(active=True)

    try:
        is_cached = "geodata" in request.session
        # get user ip and get information of the user
        if not is_cached:
            response = requests.get("https://reallyfreegeoip.org/json/%s" % ip_address)
            request.session["geodata"] = response.json()

        user = User.objects.get(username=username)
        if user.is_field_worker:
            request.session["fieldworker_id"] = user.id
            user_ip = request.session["fieldworker_id"]
            print("referral name: ", user_ip)

        geodata = request.session["geodata"]
        request.session["user_ip"] = geodata["ip"]
        request.session["country"] = geodata["country_name"]
        request.session["country_code"] = geodata["country_code"]
        request.session["region_name"] = geodata["region_name"]
        request.session["city"] = geodata["city"]
    except:
        pass

    if not request.session.get("user_ip"):
        messages.info(
            request,
            _(
                "Welcome to Bizwallet Co-Operative. Please accept our consent form below as they enable us serve you better and securely."
            ),
        )

    return render(request, "pages/home.html", {"is_cached": is_cached, "services": services})


class ServiceListView(DetailView):
    model = Services
    template_name = 'pages/services.html'
    context_object_name = 'services'
    queryset = Services.objects.filter(active=True)

    def get_object(self, queryset=None):
        return Services.objects.get(pk=self.kwargs.get("pk"))

service_detail = ServiceListView.as_view()


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            html_message = render_to_string('email/support_mail.html', {'message': message, 'from_email': from_email, 'subject': subject})

            try:
                send_mail(subject, message, from_email, ['info@bizwallet.org'], html_message=html_message, fail_silently=False)
                messages.success(request, "Your Email Has been sent successfuly")
            except BadHeaderError:
                messages.error(request, "There was an error sending yout email at the moment, please try again later.")
                # return HttpResponse('Invalid Header found')
            return redirect('home')
    return render(request, 'pages/contact.html', {'form': form})