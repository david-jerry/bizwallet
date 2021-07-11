from allauth.account.forms import SignupForm
from allauth.account.views import SignupView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

# from bizwallet.users.forms import FieldWorkerSignupForm, InvestorSignupForm
from bizwallet.users.models import FieldWorker, Investor

# from bizwallet.users.models import FieldWorker, Investor

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        recommended_users = user.fieldworkerprofile.get_recommended_users()
        context['my_recs'] = recommended_users
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


class ProfileSignupView(SignupView):
    template_name = ""
    success_url = ""
    form_class = SignupForm
    profile_class = None
    fw_bool = None

    def form_valid(self, form):
        res = super(ProfileSignupView, self).form_valid(form)
        profile = self.profile_class(user=self.user, user_is_field_worker=self.fw_bool)
        print("------profile------", profile)
        profile.save()

        return res


class InvestorSignupView(SignupView):
    template_name = "account/signup_investor.html"
    success_url = "/"
    profile_class = Investor
    fw_bool = False

investor_signup = InvestorSignupView.as_view()


class FieldWorkerSignupView(SignupView):
    template_name = "account/signup_fieldworker.html"
    success_url = "/"
    profile_class = FieldWorker
    fw_bool = True

fieldworker_signup = FieldWorkerSignupView.as_view()



# Funtion Based View for users

# def InvestorSignupView(request):
#     template_name = "account/signup_investor.html"
#     user_ip = request.session.get("user_ip")
#     user_country = request.session.get("country")
#     user_country_code = request.session.get("country_code")
#     user_city = request.session.get("city")

#     user_form = UserCreationForm(request.POST or None)
#     investor_form = InvestorSignupForm(request.POST or None)

#     if request.method == 'POST' and user_form.is_valid() and investor_form.is_valid():
#         user = user_form.save(commit=False)
#         user.country = user_country
#         user.city = user_city
#         user.ip = user_ip
#         user.is_field_worker = False
#         user.save()
#         user.investorprofile.save()
#         messages.success(request, "Investor Profile Created Successfully")
#         send_mail(
#             "NEW INVESTOR REGISTRATION Bizwallet NG",
#             f"{user.fullname} just registered with this email \n Email: {user.email}",
#             "noreply@bizwallet.org",
#             ["admin@bizwallet.org"],
#             fail_silently=False,
#         )
#     else:
#         user_form = UserCreationForm()
#         investor_form = InvestorSignupForm()
#         messages.error(request, "Investor Profile Failed to create")

#     context = {
#         "user_form": user_form,
#         'investor_form': investor_form,
#     }

#     return render(request, template_name, context)


# investor_signup = InvestorSignupView


# def FieldWorkerSignupView(request):
#     template_name = "account/signup_fieldworker.html"
#     user_ip = request.session.get("user_ip")
#     user_country = request.session.get("country")
#     user_country_code = request.session.get("country_code")
#     user_city = request.session.get("city")

#     user_form = UserCreationForm(request.POST or None)
#     fieldworker_form = FieldWorkerSignupForm(request.POST or None)

#     if request.method == 'POST' and user_form.is_valid() and fieldworker_form.is_valid():
#         user = user_form.save(commit=False)
#         user.country = user_country
#         user.city = user_city
#         user.ip = user_ip
#         user.is_field_worker = True
#         user.save()
#         user.fieldworkerprofile.save()
#         messages.success(request, "Fieldworker Profile Created Successfully")
#         send_mail(
#             "NEW FIELDWORKER REGISTRATION Bizwallet NG",
#             f"{user.fullname} just registered with this email \n Email: {user.email}",
#             "noreply@bizwallet.org",
#             ["admin@bizwallet.org"],
#             fail_silently=False,
#         )
#     else:
#         user_form = UserCreationForm()
#         fieldworker_form = FieldWorkerSignupForm()
#         messages.error(request, "Fieldworker Profile Failed to create")

#     context = {
#         "user_form": user_form,
#         'fieldworker_form': fieldworker_form,
#     }



#     return render(request, template_name, context)

# fieldworker_signup = FieldWorkerSignupView
