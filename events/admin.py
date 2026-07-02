from django.contrib import admin
from .models import Brand, Event


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "instagram")
    search_fields = ("name", "slug", "instagram")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "slug", "active", "max_initial_attempts", "max_extra_attempts")
    list_filter = ("active", "brand")
    search_fields = ("name", "slug", "brand__name")
    prepopulated_fields = {"slug": ("name",)}