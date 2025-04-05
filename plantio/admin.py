from django.contrib import admin
from .models import Led, Device, SensorType, Sensor

# Register your models here.
admin.site.register(Led)
admin.site.register(Device)
admin.site.register(SensorType)
admin.site.register(Sensor)
