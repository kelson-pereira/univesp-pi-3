import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.http import JsonResponse
from .models import Led, Device, SensorType, Sensor

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
    sensors = Sensor.objects.all()
    return render(request, "led_control.html", {"led": led, "sensors": sensors})

@csrf_exempt
def sensor_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mac_address = data.get('mac')
        device, _ = Device.objects.get_or_create(mac_address=mac_address)
        values = {key: float(value) for key, value in data.items() if key != 'mac'}
        for key, value in values.items():
            sensor_type, _ = SensorType.objects.get_or_create(name=key)
            sensor, created = Sensor.objects.get_or_create(sensor_type=sensor_type, device=device, defaults={'value': value, 'status': True})
            if not created:
                sensor.value = value
                sensor.status = True
                sensor.save()
        return JsonResponse({"status": "success"})