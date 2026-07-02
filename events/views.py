from django.shortcuts import render, get_object_or_404, redirect
from events.models import Event
from players.models import Player
from games.models import Game, Attempt, generate_code
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def event_register(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug, active=True)
    game = Game.objects.filter(active=True).first()

    if request.method == "POST":
        player = Player.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone", ""),
            neighborhood=request.POST.get("neighborhood", ""),
        )

        attempt = Attempt.objects.create(
            event=event,
            player=player,
            game=game,
            code=generate_code(),
            reason="initial",
        )

        return render(request, "events/code.html", {
            "event": event,
            "attempt": attempt,
        })

    return render(request, "events/register.html", {
        "event": event,
    })


def tv_screen(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug, active=True)

    return render(request, "events/tv.html", {
        "event": event,
    })


def ranking(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug, active=True)

    attempts = Attempt.objects.filter(
        event=event,
        status="finished",
    ).order_by("-score")[:20]

    return render(request, "events/ranking.html", {
        "event": event,
        "attempts": attempts,
    })


@csrf_exempt
def validate_code(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug, active=True)

    data = json.loads(request.body)
    code = data.get("code")

    try:
        attempt = Attempt.objects.get(
            event=event,
            code=code,
            status="generated",
        )
        attempt.start()

        return JsonResponse({
            "ok": True,
            "attempt_id": attempt.id,
            "player_name": attempt.player.name,
        })

    except Attempt.DoesNotExist:
        return JsonResponse({
            "ok": False,
            "error": "Código inválido ou já utilizado.",
        })


@csrf_exempt
def save_score(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug, active=True)

    data = json.loads(request.body)
    attempt_id = data.get("attempt_id")
    score = data.get("score", 0)

    try:
        attempt = Attempt.objects.get(
            id=attempt_id,
            event=event,
            status="playing",
        )
        attempt.finish(score)

        return JsonResponse({"ok": True})

    except Attempt.DoesNotExist:
        return JsonResponse({
            "ok": False,
            "error": "Tentativa não encontrada.",
        })