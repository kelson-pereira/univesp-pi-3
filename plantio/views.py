from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.http import JsonResponse
from .models import Led

# Crie suas visualizações aqui.

def home(request):
    return render(request, 'home.html')

def led_status(request):
    led = Led.objects.first()
    return JsonResponse({'status': led.status})