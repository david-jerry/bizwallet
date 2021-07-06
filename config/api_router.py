from __future__ import absolute_import

from django.conf import settings
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# To documentation api
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter, SimpleRouter

# To get and refresh token for authenticated api views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from bizwallet.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls


# Swgger url to access documentation for api
schema_view = get_schema_view(
    openapi.Info(
        title="Bizwallet NG Rest API v1",
        default_version="v1",
        description="Get Endpoint to Bizwallet NG Rest API. Ensure to get your accessToken/APIKey.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@bizwallet.ng"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Swagger API Documentation routes
urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "documentation/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
