from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from django.utils.html import format_html
from django.utils.safestring import mark_safe
from bizwallet.utils.export_as_csv import ExportCsvMixin

from bizwallet.users.forms import ProfileForm, SubscribeForm, UserChangeForm, UserCreationForm, PlanForm, KinForm
from bizwallet.users.models import Profile, NextOfKin, EnrollmentPlan, Subscribe, Testimonial

User = get_user_model()



class ProfileAdmin(admin.StackedInline):
    form = ProfileForm
    model = Profile

    def __init__(self, parent_model, admin_site):
        self.fk_name = getattr(self.model, 'fk_name', None)
        super().__init__(parent_model, admin_site)


# class SubcribeAdmin(admin.StackedInline):
#     form = SubscribeForm
#     model = Subscribe

#     def __init__(self, parent_model, admin_site):
#         self.fk_name = getattr(self.model, 'fk_name', None)
#         super().__init__(parent_model, admin_site)



@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ExportCsvMixin):

    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [ProfileAdmin]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "image",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "gender",
                    "marital",
                    "dob",
                    "state",
                )
            },
        ),
        (
            _("Subscription info"),
            {
                "fields": (
                    "plan",
                )
            },
        ),
        (
            _("Career info"),
            {
                "fields": (
                    "occupation",
                    "office_address",
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
    actions = [
        "export_as_csv",
    ]


admin.site.register(Profile)
admin.site.register(Testimonial)
admin.site.register(NextOfKin)


class PlanAdmin(admin.ModelAdmin, ExportCsvMixin):
    form = PlanForm
    model = EnrollmentPlan
    list_per_page = 250
    empty_value_display = '-empty-'
    search_fields = ["__str__"]
    list_display = [
        "__str__",
        'title',
        "percentage",
        "invest",
        'status',
        'duration'
    ]
    list_editable = [
        'title',
        "percentage",
        "invest",
        'status',
        'duration'
    ]
    actions = [
        "export_as_csv",
    ]

admin.site.register(EnrollmentPlan, PlanAdmin)


class SubAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Subscribe
    list_per_page = 250
    empty_value_display = '-empty-'
    search_fields = ["__str__"]
    list_display = ["__str__", 'bill']
    actions = [
        "export_as_csv",
    ]

admin.site.register(Subscribe, SubAdmin)
