from django.db import models
from datetime import time

# Crie seus modelos aqui.


class Led(models.Model):
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Device(models.Model):
    mac_address = models.CharField(primary_key=True, max_length=17, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SensorType(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    description = models.TextField()
    unit = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Sensor(models.Model):
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.FloatField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ControlType(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Control(models.Model):
    control_type = models.ForeignKey(ControlType, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    schedule_enabled = models.BooleanField(default=False)
    start_time = models.TimeField(default=time(6,0))
    interval_on_minutes = models.PositiveIntegerField(default=960)  # tempo ligado
    interval_off_minutes = models.PositiveIntegerField(default=0)  # tempo desligado
    repeat_count = models.PositiveIntegerField(default=1)  # 0 = infinito
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)