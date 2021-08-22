from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from bizwallet.users.forms import (  # PlanForm,; SubscribeForm,
    KinForm,
    ProfileForm,
    UserChangeForm,
    UserCreationForm,
)
from bizwallet.users.models import (  # Subscribe, EnrollmentPlan
    BalHistory,
    LoginHistory,
    Membership,
    MembershipFeature,
    NextOfKin,
    PayHistory,
    Profile,
    Subscription,
    Testimonial,
    UserMembership,
    Withdrawals,
)
from bizwallet.utils.export_as_csv import ExportCsvMixin

User = get_user_model()

admin.site.register(Withdrawals)
admin.site.register(BalHistory)
admin.site.register(MembershipFeature)
admin.site.register(UserMembership)
admin.site.register(LoginHistory)
admin.site.register(PayHistory)

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
        "has_paid",
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


class MembershipAdmin(admin.ModelAdmin, ExportCsvMixin):
    # form = PlanForm
    model = Membership
    list_per_page = 250
    empty_value_display = '-empty-'
    search_fields = ["__str__"]
    list_display = [
        "__str__",
        'membership_type',
        "duration",
        "price",
        'created',
        'modified'
    ]
    list_editable = [
        'membership_type',
    ]
    actions = [
        "export_as_csv",
    ]

admin.site.register(Membership, MembershipAdmin)


class SubAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Subscription
    list_per_page = 250
    empty_value_display = '-empty-'
    search_fields = ["__str__"]
    list_display = ["__str__", 'expires_in', 'active']
    list_editable = ['active']
    actions = [
        "export_as_csv",
    ]

admin.site.register(Subscription, SubAdmin)
