from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from bizwallet.utils.export_as_csv import ExportCsvMixin

from .models import Category, Image, Post


# Register your models here.
class PostImagesInline(admin.StackedInline):
    model = Image

class PostModelAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["title", "videos", "created", "featured"]
    list_display_links = ["created"]
    list_editable = ["title", "featured"]
    search_fields = ["title", "content"]
    inlines = [PostImagesInline]
    list_per_page = 250
    actions = [
        "export_as_csv",
        "mark_all_posts",
        "mark_all_featured_posts",
        "mark_all_posts_by_me",
    ]


    class Meta:
        model = Post

    def mark_all_posts(self, request, queryset):
        queryset.update(draft=False)

    def mark_all_featured_posts(self, request, queryset):
        queryset.update(draft=False, featured=True)

    def mark_all_posts_by_me(self, request, queryset):
        user = request.user
        queryset.update(author=user)

    def image(self, obj):
        return mark_safe(
            '<img src="{url}" width="120px" height="auto" />'.format(
                url=obj.image.image.url,
            )
        )

    def save_model(self, request, obj, form, change):
        if change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostModelAdmin)
