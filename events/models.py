from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    instagram = models.CharField(max_length=120, blank=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    max_initial_attempts = models.PositiveIntegerField(default=1)
    max_extra_attempts = models.PositiveIntegerField(default=2)

    promoter_pin = models.CharField(max_length=6, default="4825")

    def __str__(self):
        return f"{self.brand.name} - {self.name}"