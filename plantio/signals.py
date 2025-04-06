from .models import SensorType

def create_sensor_type(sender, **kwargs):
    sensor_types = [
        {
            "name": "tmpA",
            "description": "Temperatura ambiente",
            "unit": "°C"
        },
        {
            "name": "umdA",
            "description": "Umidade relativa do ar",
            "unit": "%"
        },
        {
            "name": "tmpS",
            "description": "Temperatura da solução nutritiva",
            "unit": "°C"
        }
    ]
    for sensor in sensor_types:
        SensorType.objects.get_or_create(name=sensor['name'],description=sensor['description'],unit=sensor['unit'])