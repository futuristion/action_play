from django.contrib import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "neighborhood", "instagram_confirmed", "created_at")
    search_fields = ("name", "phone", "neighborhood")
    list_filter = ("instagram_confirmed", "neighborhood")