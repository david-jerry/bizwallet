from django.urls import path

from bizwallet.core.views import service_detail

app_name = "services"
urlpatterns = [
    path("<str:title>/", view=service_detail, name="detail"),
]