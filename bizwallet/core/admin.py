from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.urls import reverse
from tinymce.widgets import TinyMCE


class CustomFlatPageAdmin(FlatPageAdmin):
    """
    FlatPage Admin
    """

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "content":
            return db_field.formfield(
                widget=TinyMCE(
                    attrs={"cols": 60, "rows": 10},
                    mce_attrs={"external_link_list_url": reverse("tinymce-linklist")},
                )
            )
        return super().formfield_for_dbfield(db_field, **kwargs)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)
