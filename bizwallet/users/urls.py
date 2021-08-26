from django.urls import path, re_path

from bizwallet.users.views import (  # subscribe_view,
    BankUpdateView,
    NotificationView,
    TopWalletViews,
    UpdatePhotoView,
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
    path("~dp-update/", view=UpdatePhotoView.as_view(), name="photo"),
    path("~bank-update/", view=BankUpdateView.as_view(), name="bank"),
    path("~add-kin/", view=kin_creation, name="kin"),
    path("~top-up/", view=TopWalletViews.as_view(), name="topup"),
    path("~withdraw/", view=WithdrawalView.as_view(), name="withdraw"),
    path("~subscribe/", view=subscribe, name="subscribe"),
    path("~notification/", view=NotificationView.as_view(), name="notif"),
    re_path("~payment/$", view=call_back_url, name="payment"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
