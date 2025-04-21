import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from .models import Led, Device, SensorType, Sensor, ControlType, Control
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Crie suas visualizações aqui.


def home(request):
    devices = Device.objects.all()
    print('OK' + str(devices.count()))
    return render(request, "home.html", {"devices": devices})


@csrf_exempt
def dashboard(request, id):
    led = Led.objects.first()
    device = Device.objects.get(mac_address=id)
    controls = Control.objects.filter(device_id=id)
    sensors = Sensor.objects.filter(device_id=id)
    updated_now = (timezone.now() - device.updated_at).total_seconds() < 60
    return render(
        request,
        "dashboard.html",
        {
            "led": led,
            "status": led.status if led else False,
            "device": device,
            "updated_now": updated_now,
            "controls": controls,
            "sensors": sensors,
        },
    )


@csrf_exempt
def controls(request):
    if request.method == 'GET':
        data = json.loads(request.body)
        mac_address = data.get('mac')
        device, _ = Device.objects.update_or_create(mac_address=mac_address)
        controls = Control.objects.filter(device_id=mac_address)
        response_json = {}
        for control in controls:
            status = get_control_status(control)
            response_json[control.control_type.name] = status
        return JsonResponse(response_json)
    elif request.method == 'POST':
        data = json.loads(request.body)
        mac_address = data.get('mac')
        device, _ = Device.objects.update_or_create(mac_address=mac_address)
        for control in data['controls']:
            control_type = ControlType.objects.get(name=control.get('type'))
            Control.objects.update_or_create(
                device=device,
                control_type=control_type,
                defaults={
                    'status': control.get('status', False),
                    'schedule_enabled': control.get('schedule_enabled', False),
                    'start_time': control.get('start_time'),
                    'interval_on_minutes': control.get('interval_on_minutes'),
                    'interval_off_minutes': control.get('interval_off_minutes'),
                    'repeat_count': control.get('repeat_count', 0)
                }
            )
        return JsonResponse({'status': 'success'})


@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mac_address = data.get('mac')
        device, _ = Device.objects.update_or_create(mac_address=mac_address)
        if "controls" in data:
            for control in data['controls']:
                control_type = ControlType.objects.get(name=control.get('type'))
                Control.objects.update_or_create(
                    device=device,
                    control_type=control_type,
                    defaults={
                        'status': control.get('status', False),
                        'schedule_enabled': control.get('schedule_enabled', False),
                        'start_time': control.get('start_time'),
                        'interval_on_minutes': control.get('interval_on_minutes'),
                        'interval_off_minutes': control.get('interval_off_minutes'),
                        'repeat_count': control.get('repeat_count', 0)
                    }
                )
        if "sensors" in data:
            for sensor in data['sensors']:
                sensor_type = SensorType.objects.get(name=sensor.get('type'))
                Sensor.objects.update_or_create(
                    device=device,
                    sensor_type=sensor_type,
                    defaults={"value": sensor.get('value'), "status": True},
                )
        controls = Control.objects.filter(device_id=mac_address)
        response_json = {}
        for control in controls:
            new_status = get_control_status(control)
            if control.status != new_status:  # só atualiza se mudou
                control.status = new_status
                control.save(update_fields=['status'])
                channel_layer = get_channel_layer() # notificar via WebSocket
                async_to_sync(channel_layer.group_send)(
                    f"device_{control.device.mac_address.replace(":","-")}",
                    {
                        "type": "control_status_update",
                        "control_name": control.control_type.name,
                        "status": new_status
                    }
                )
            response_json[control.control_type.name] = new_status
        return JsonResponse(response_json)


def get_control_status(control):
    current_time = timezone.now().time()
    if not control.schedule_enabled:
        return 0
    start_minutes = control.start_time.hour * 60 + control.start_time.minute
    current_minutes = current_time.hour * 60 + current_time.minute
    if current_minutes < start_minutes:
        return 0 # se ainda não chegou no horário de início
    elapsed_minutes = current_minutes - start_minutes
    # se não há intervalo desligado (ciclo contínuo)
    if not control.interval_off_minutes:
        return 1 if elapsed_minutes < control.interval_on_minutes else 0
    # ciclo completo
    total_cycle = control.interval_on_minutes + control.interval_off_minutes
    # se não há repetições ou ainda está dentro do número de ciclos
    if control.repeat_count == 0 or \
       (elapsed_minutes // total_cycle) < control.repeat_count:
        cycle_position = elapsed_minutes % total_cycle
        return 1 if cycle_position < control.interval_on_minutes else 0
    return 0 # se excedeu o número de repetições


def scheduler_controls(request):
    controls = Control.objects.filter(schedule_enabled=True)
    for control in controls:
        new_status = get_control_status(control)
        if control.status != new_status:  # só atualiza se mudou
            control.status = new_status
            control.save(update_fields=['status'])
            
            # notificar via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"device_{control.device.mac_address.replace(":","-")}",
                {
                    "type": "control_status_update",
                    "control_name": control.control_type.name,
                    "status": new_status
                }
            )
    return JsonResponse({'status': 'success'})


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
        device, _ = Device.objects.update_or_create(mac_address=mac_address)
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
