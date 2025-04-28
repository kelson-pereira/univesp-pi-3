import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *

# Crie suas visualizações aqui.


def home(request):
    devices = Device.objects.all()
    return render(request, "home.html", {"devices": devices})


@csrf_exempt
def dashboard(request, id):
    device = Device.objects.get(mac_address=id)
    controls = Control.objects.filter(device_id=id).order_by('id')
    for control in controls:
        new_status = get_control_status(control)
        if control.status != new_status:  # só atualiza se mudou
            control.status = new_status
            control.save(update_fields=['status'])
    sensors = Sensor.objects.filter(device_id=id)
    updated_now = (timezone.now() - device.updated_at).total_seconds() < 60
    return render(request, "dashboard.html", {"device": device, "updated_now": updated_now, "controls": controls, "sensors": sensors})


@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mac_address = data.get('mac')
        device, _ = Device.objects.update_or_create(mac_address=mac_address)
        updated_now = (timezone.now() - device.updated_at).total_seconds() < 60
        channel_layer = get_channel_layer() # notificar via websocket
        async_to_sync(channel_layer.group_send)(
            f"dashboard_{device.mac_address.replace(':','-')}",
            {
                "type": "device_update",
                "updated_now": updated_now,
                "updated_at": device.updated_at.isoformat()
            }
        )
        if "controls" in data:
            for control in data['controls']:
                control_type = ControlType.objects.get(name=control.get('type'))
                naive_time = datetime.strptime(control.get('start_time'), '%H:%M:%S').time()
                local_now = timezone.localtime(timezone.now())
                local_dt = timezone.make_aware(
                    datetime.combine(local_now.date(), naive_time),
                    timezone.get_current_timezone()
                )
                utc_zone = getattr(timezone, 'UTC', None) or getattr(timezone, 'utc', None)
                Control.objects.update_or_create(
                    device=device,
                    control_type=control_type,
                    defaults={
                        'status': control.get('status', False),
                        'schedule_enabled': control.get('schedule_enabled', False),
                        'start_time': local_dt.astimezone(utc_zone).time(),
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
                channel_layer = get_channel_layer() # notificar via websocket
                async_to_sync(channel_layer.group_send)(
                    f"dashboard_{device.mac_address.replace(':','-')}",
                    {
                        "type": "sensor_update",
                        "sensor_type": sensor_type.name,
                        "value": sensor.get('value'),
                        "status": True
                    }
                )
        response_json = {}
        controls = Control.objects.filter(device_id=mac_address)
        for control in controls:
            new_status = get_control_status(control)
            if control.status != new_status:  # só atualiza se mudou
                control.status = new_status
                control.save(update_fields=['status'])
            channel_layer = get_channel_layer() # notificar via websocket
            async_to_sync(channel_layer.group_send)(
                f"dashboard_{device.mac_address.replace(':','-')}",
                {
                    "type": "control_update",
                    "control_type": control.control_type.name,
                    "schedule_enabled": control.schedule_enabled,
                    "status": new_status
                }
            )
            response_json[control.control_type.name] = new_status
        sensors = Sensor.objects.filter(device_id=mac_address)
        for sensor in sensors:
            response_json[sensor.sensor_type.name] = sensor.value
            response_json[sensor.sensor_type.name + '_min'] = sensor.sensor_type.min_value
            response_json[sensor.sensor_type.name + '_max'] = sensor.sensor_type.max_value
        return JsonResponse(response_json)


@csrf_exempt
@require_POST
def update_schedule(request):
    try:
        device_id = request.POST.get('device_id')
        control_name = request.POST.get('control_name')
        control = Control.objects.get(device__mac_address=device_id, control_type__name=control_name)
        control.start_time = request.POST.get('start_time')
        control.interval_on_minutes = request.POST.get('interval_on_minutes')
        control.interval_off_minutes = request.POST.get('interval_off_minutes')
        control.repeat_count = request.POST.get('repeat_count')
        control.save()
        
        return redirect('dashboard', id=device_id)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@require_POST
def update_schedule_status(request):
    try:
        data = json.loads(request.body)
        control = Control.objects.get(
            device__mac_address=data['device_id'],
            control_type__name=data['control_name']
        )
        control.schedule_enabled = data['schedule_enabled']
        control.save(update_fields=['schedule_enabled'])
        new_status = get_control_status(control)
        if control.status != new_status:  # só atualiza se mudou
                control.status = new_status
                control.save(update_fields=['status'])
        channel_layer = get_channel_layer() # notificar via websocket
        async_to_sync(channel_layer.group_send)(
            f"dashboard_{data['device_id'].replace(':','-')}",
            {
                "type": "control_update",
                "control_type": control.control_type.name,
                "schedule_enabled": control.schedule_enabled,
                "status": new_status
            }
        )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
def update_control_status(request):
    try:
        data = json.loads(request.body)
        control = Control.objects.get(
            device__mac_address=data['device_id'],
            control_type__name=data['control_name']
        )
        control.status = data['status']
        control.save(update_fields=['status'])
        channel_layer = get_channel_layer() # notificar via websocket
        async_to_sync(channel_layer.group_send)(
            f"dashboard_{data['device_id'].replace(':','-')}",
            {
                "type": "control_update",
                "control_type": control.control_type.name,
                "schedule_enabled": control.schedule_enabled,
                "status": control.status
            }
        )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def get_control_status(control):
    # Obtém o horário local atual considerando o timezone
    now = timezone.localtime(timezone.now())
    current_time = now.time()
    if not control.schedule_enabled:
        return control.status
    start_minutes = control.start_time.hour * 60 + control.start_time.minute
    current_minutes = current_time.hour * 60 + current_time.minute
    if current_minutes < start_minutes:
        return False # se ainda não chegou no horário de início
    elapsed_minutes = current_minutes - start_minutes
    # se não há intervalo desligado (ciclo contínuo)
    if not control.interval_off_minutes:
        return True if elapsed_minutes < control.interval_on_minutes else False
    # ciclo completo
    total_cycle = control.interval_on_minutes + control.interval_off_minutes
    # se não há repetições ou ainda está dentro do número de ciclos
    if control.repeat_count == 0 or \
       (elapsed_minutes // total_cycle) < control.repeat_count:
        cycle_position = elapsed_minutes % total_cycle
        return True if cycle_position < control.interval_on_minutes else False
    return False # se excedeu o número de repetições


def scheduler_controls(request):
    controls = Control.objects.filter(schedule_enabled=True)
    for control in controls:
        new_status = get_control_status(control)
        if control.status != new_status:  # só atualiza se mudou
            control.status = new_status
            control.save(update_fields=['status'])
        channel_layer = get_channel_layer() # notificar via websocket
        async_to_sync(channel_layer.group_send)(
            f"dashboard_{control.device.mac_address.replace(':','-')}",
            {
                "type": "control_update",
                "control_type": control.control_type.name,
                "schedule_enabled": control.schedule_enabled,
                "status": new_status
            }
        )
    return JsonResponse({'status': 'success'})
