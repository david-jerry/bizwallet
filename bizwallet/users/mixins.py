from allauth.account.forms import SignupForm
from allauth.account.views import SignupView

from bizwallet.users.models import Profile

class ProfileSignupView(SignupView):
    template_name = ""
    success_url = ""
    form_class = SignupForm
    profile_class = Profile
    fw_bool = None

    def form_valid(self, form):
        res = super(ProfileSignupView, self).form_valid(form)
        profile = self.profile_class(user=self.user, user_is_field_worker=self.fw_bool)
        print("------profile------", profile)
        res.save()
        profile.save()

        return res




