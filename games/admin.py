from django.contrib import admin
from .models import Game, Attempt


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "active")
    search_fields = ("name", "slug")
    list_filter = ("active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("code", "player", "event", "game", "status", "reason", "score", "released_by_promoter", "created_at")
    list_filter = ("status", "reason", "event", "game", "released_by_promoter")
    search_fields = ("code", "player__name", "player__phone", "player__email")