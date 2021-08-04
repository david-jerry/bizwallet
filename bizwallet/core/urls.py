from django.urls import path

from bizwallet.core.views import email_subscribe, service_detail

app_name = "services"
urlpatterns = [
    path("<int:pk>/", view=service_detail, name="detail"),
    path("subscribe/", view=email_subscribe, name="subscribe"),
]
