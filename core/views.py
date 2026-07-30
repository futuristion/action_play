from django.shortcuts import render

from events.models import Event


def home(request):
    events = (
        Event.objects
        .filter(active=True)
        .select_related("brand")
        .order_by("-created_at")
    )

    return render(
        request,
        "core/home.html",
        {
            "events": events,
        },
    )