from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    instagram_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name