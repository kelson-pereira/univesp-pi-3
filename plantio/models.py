from django.db import models

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