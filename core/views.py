from django.shortcuts import render
from django.shortcuts import redirect


def home(request):
    return redirect("event_register", event_slug="cafe-terra-brasil")

