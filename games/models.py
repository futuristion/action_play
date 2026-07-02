from django.db import models
from django.utils import timezone
from events.models import Event
from players.models import Player
import random


class Game(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Attempt(models.Model):
    STATUS_CHOICES = [
        ("generated", "Gerado"),
        ("playing", "Jogando"),
        ("finished", "Finalizado"),
        ("expired", "Expirado"),
    ]

    EXTRA_REASON_CHOICES = [
        ("initial", "Tentativa Inicial"),
        ("instagram", "Seguiu Instagram"),
        ("courtesy", "Cortesia"),
        ("purchase", "Compra"),
        ("vip", "VIP"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    code = models.CharField(max_length=4, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="generated")
    reason = models.CharField(max_length=20, choices=EXTRA_REASON_CHOICES, default="initial")

    score = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    released_by_promoter = models.BooleanField(default=False)

    def start(self):
        self.status = "playing"
        self.started_at = timezone.now()
        self.save()

    def finish(self, score):
        self.status = "finished"
        self.score = score
        self.finished_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.code} - {self.player.name}"


def generate_code():
    while True:
        code = str(random.randint(1000, 9999))
        if not Attempt.objects.filter(code=code, status__in=["generated", "playing"]).exists():
            return code