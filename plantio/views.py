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

def toggle_led(request):
    led, _ = Led.objects.get_or_create(id=1)
    led.status = not led.status
    led.save()
    return JsonResponse({"led": led.status})

def led_control_view(request):
    led = Led.objects.first()
    return render(request, "led_control.html", {"status": led.status if led else False})