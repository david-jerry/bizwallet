from django.urls import path

from bizwallet.users.views import (
    kin_creation,
    subscribe_view,
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~add-kin/", view=kin_creation, name="kin"),
    path("~subscribe/", view=subscribe_view, name="subscribe"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
