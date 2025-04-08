import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from .models import Led, Device, SensorType, Sensor
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Crie suas visualizações aqui.


def home(request):
    devices = Device.objects.all()
    return render(request, "home.html", {"devices": devices})


@csrf_exempt
def dashboard(request, id):
    led = Led.objects.first()
    sensors = Sensor.objects.filter(device_id=id)
    return render(
        request,
        "dashboard.html",
        {
            "led": led,
            "device_id": id,
            "status": led.status if led else False,
            "sensors": sensors,
        },
    )


def led_status(request):
    led = Led.objects.first()
    return JsonResponse({"status": led.status})


@csrf_exempt
def toggle_led(request):
    led, _ = Led.objects.get_or_create(id=1)
    led.status = not led.status
    led.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "led_control", {"type": "led_status_update", "status": led.status}
    )
    return JsonResponse({"led": led.status})


@csrf_exempt
def led_control_view(request):
    led = Led.objects.first()
    sensors = Sensor.objects.all()
    return render(
        request,
        "led_control.html",
        {"led": led, "status": led.status if led else False, "sensors": sensors},
    )


@csrf_exempt
def sensor_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        mac_address = data.get("mac")
        device, _ = Device.objects.get_or_create(mac_address=mac_address)
        values = {key: float(value) for key, value in data.items() if key != "mac"}
        for key, value in values.items():
            sensor_type, _ = SensorType.objects.get_or_create(name=key)
            sensor, created = Sensor.objects.get_or_create(
                sensor_type=sensor_type,
                device=device,
                defaults={"value": value, "status": True},
            )
            if not created:
                sensor.value = value
                sensor.status = True
                sensor.save()
        return JsonResponse({"status": "success"})
