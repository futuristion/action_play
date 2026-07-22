from django.shortcuts import render, get_object_or_404, redirect
from events.models import Event
from players.models import Player
from games.models import Game, Attempt, generate_code
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import qrcode
import base64
from io import BytesIO
import re
from django.contrib import messages


def event_register(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug, active=True)
    game = Game.objects.filter(active=True).first()

    if request.method == "POST":
        phone = re.sub(r"\D", "", request.POST.get("phone", ""))
        name = request.POST.get("name", "").strip()
        neighborhood = request.POST.get("neighborhood", "").strip()

        # Validação do telefone
        if len(phone) != 11:
            return render(request, "events/register.html", {
                "event": event,
                "error": "Informe um telefone válido com DDD.",
            })

        # Verifica se o telefone já está cadastrado
        existing_player = Player.objects.filter(phone=phone).first()

        if existing_player:
            return render(request, "events/register.html", {
                "event": event,
                "error": (
                    f"Este telefone já está cadastrado para "
                    f"{existing_player.name}. Procure o promotor "
                    "para liberar uma nova tentativa."
                ),
            })

        # Só cria jogador quando o telefone é novo
        player = Player.objects.create(
            phone=phone,
            name=name,
            neighborhood=neighborhood,
        )

        attempt = Attempt.objects.create(
            event=event,
            player=player,
            game=game,
            code=generate_code(),
            reason="initial",
        )

        return redirect(
            "code_screen",
            event_slug=event.slug,
            attempt_id=attempt.id,
        )

    return render(request, "events/register.html", {
        "event": event,
    })


def tv_screen(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug, active=True)

    register_url = request.build_absolute_uri(
        f"/e/{event.slug}/"
    )

    qr = qrcode.make(register_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "events/tv.html", {
        "event": event,
        "register_url": register_url,
        "qr_base64": qr_base64,
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
    

def code_screen(request, event_slug, attempt_id):
    event = get_object_or_404(Event, slug=event_slug, active=True)

    attempt = get_object_or_404(
        Attempt,
        id=attempt_id,
        event=event,
    )

    return render(request, "events/code.html", {
        "event": event,
        "attempt": attempt,
    })


def operator_panel(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug, active=True)

    query = request.GET.get("q", "")

    players = Player.objects.all().order_by("-created_at")

    if query:
        players = players.filter(
            name__icontains=query
        ) | players.filter(
            phone__icontains=query
        )

    players = players[:30]

    return render(request, "events/operator.html", {
        "event": event,
        "players": players,
        "query": query,
    })


def release_attempt(request, event_slug, player_id):
    event = get_object_or_404(Event, slug=event_slug, active=True)
    player = get_object_or_404(Player, id=player_id)
    game = Game.objects.filter(active=True).first()

    if request.method == "POST":
        pin = request.POST.get("pin")

        if pin != event.promoter_pin:
            return redirect("operator_panel", event_slug=event.slug)

        attempt = Attempt.objects.create(
            event=event,
            player=player,
            game=game,
            code=generate_code(),
            reason="instagram",
            released_by_promoter=True,
        )

        return redirect("code_screen", event_slug=event.slug, attempt_id=attempt.id)

    return redirect("operator_panel", event_slug=event.slug)

def ranking_json(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug, active=True)

    attempts = Attempt.objects.filter(
        event=event,
        status="finished",
    ).order_by("-score")[:5]

    data = []

    for attempt in attempts:
        data.append({
            "player": attempt.player.name,
            "neighborhood": attempt.player.neighborhood,
            "score": attempt.score,
        })

    return JsonResponse({
        "ok": True,
        "ranking": data,
    })