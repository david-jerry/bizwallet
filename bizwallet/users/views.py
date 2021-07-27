from django.urls.base import reverse_lazy
from allauth.account.forms import SignupForm
from allauth.account.views import SignupView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from bizwallet.users.forms import FieldWorkerSignupForm, InvestorSignupForm
from bizwallet.users.models import Profile

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
    success_url = reverse_lazy("home")
    form_class = InvestorSignupForm

investor_signup = InvestorSignupView.as_view()


class FieldWorkerSignupView(SignupView):
    template_name = "account/signup_fieldworker.html"
    success_url = reverse_lazy("home")
    form_class = FieldWorkerSignupForm

fieldworker_signup = FieldWorkerSignupView.as_view()


