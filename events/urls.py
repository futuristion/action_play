from django.urls import path
from . import views


urlpatterns = [
    path("e/<slug:event_slug>/", views.event_register, name="event_register"),
    path("e/<slug:event_slug>/tv/", views.tv_screen, name="tv_screen"),
    path("e/<slug:event_slug>/ranking/", views.ranking, name="ranking"),

    path("api/e/<slug:event_slug>/validate-code/", views.validate_code, name="validate_code"),
    path("api/e/<slug:event_slug>/save-score/", views.save_score, name="save_score"),
]