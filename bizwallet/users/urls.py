from django.urls import path, re_path

from bizwallet.users.views import (  # subscribe_view,
    WithdrawalView,
    call_back_url,
    kin_creation,
    subscribe,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~add-kin/", view=kin_creation, name="kin"),
    path("~withdraw/", view=WithdrawalView.as_view(), name="withdraw"),
    path("~subscribe/", view=subscribe, name="subscribe"),
    re_path("~payment/$", view=call_back_url, name="payment"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
