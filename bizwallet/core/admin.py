from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.urls import reverse
from tinymce.widgets import TinyMCE
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from bizwallet.utils.export_as_csv import ExportCsvMixin

from .forms import ServicesForm, ServicesVariationForm
from .models import Services, ServicesVariations

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


class ServiceVariationAdmin(admin.StackedInline):
    form = ServicesVariationForm
    model = ServicesVariations

    def __init__(self, parent_model, admin_site):
        self.fk_name = getattr(self.model, 'fk_name', None)
        super().__init__(parent_model, admin_site)


class ServicesAdmin(admin.ModelAdmin, ExportCsvMixin):
    form = ServicesForm
    model = Services
    inlines = [ServiceVariationAdmin]
    list_per_page = 250
    empty_value_display = '-empty-'
    search_fields = ["__str__"]
    list_display = [
        '__str__',
        "title",
        "description",
        # "var_title",
        # "variation_active",
        "active",
    ]
    list_display_links = ['__str__']
    list_editable = [
        "title",
        "description",
        "active"
    ]
    actions = [
        "export_as_csv",
    ]

    # def var_title(self, obj):
    #     if obj.servicevariation.title:
    #         title = obj.servicevariation.title
    #         return title
    #     else:
    #         pass

    # def variation_active(self, obj):
    #     if obj.servicevariation.active:
    #         active = obj.servicevariation.active
    #         if active:
    #             return format_html("<input type='checkbox' checked>")
    #         else:
    #             return format_html("<input type='checkbox'>")
    #     else:
    #         pass


admin.site.register(Services, ServicesAdmin)



