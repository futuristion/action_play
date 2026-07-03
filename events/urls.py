from django.urls import path
from . import views


urlpatterns = [
    path("e/<slug:event_slug>/", views.event_register, name="event_register"),
    path("e/<slug:event_slug>/tv/", views.tv_screen, name="tv_screen"),
    path("e/<slug:event_slug>/ranking/", views.ranking, name="ranking"),
    path("e/<slug:event_slug>/code/<int:attempt_id>/", views.code_screen, name="code_screen"),

    path("api/e/<slug:event_slug>/validate-code/", views.validate_code, name="validate_code"),
    path("api/e/<slug:event_slug>/save-score/", views.save_score, name="save_score"),

    path("e/<slug:event_slug>/operator/", views.operator_panel, name="operator_panel"),
    path("e/<slug:event_slug>/operator/release/<int:player_id>/", views.release_attempt, name="release_attempt"),
    
]