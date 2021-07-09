from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from bizwallet.users.forms import UserChangeForm, UserCreationForm
from bizwallet.users.models import FieldWorker, Investor

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "marital",
                    "dob",
                    "state",
                )
            },
        ),
        (
            _("Contact info"),
            {"fields": ("email", "phone_no", "country", "city", "address")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "has_paid",
                    "accept_terms",
                    "is_field_worker",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "ip",
        "username",
        "first_name",
        "last_name",
        "country",
        "city",
        "balance",
        "has_paid",
        "accept_terms",
        "is_field_worker",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_editable = [
        "first_name",
        "last_name",
        "balance",
        "has_paid",
        "accept_terms",
        "is_field_worker",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    search_fields = ["username", "first_name", "last_name"]


admin.site.register(Investor)
admin.site.register(FieldWorker)
