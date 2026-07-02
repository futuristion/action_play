from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    neighborhood = models.CharField(max_length=80, blank=True, default="")

    instagram_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name}/{self.state}"
    
class Neighborhood(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name