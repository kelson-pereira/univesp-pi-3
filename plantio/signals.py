from .models import SensorType, ControlType


def create_sensor_type(sender, **kwargs):
    sensor_types = [
        {"name": "tmpA", "description": "Temperatura ambiente", "unit": "°C"},
        {"name": "umdA", "description": "Umidade relativa do ar", "unit": "%"},
        {
            "name": "tmpS",
            "description": "Temperatura da solução nutritiva",
            "unit": "°C",
        },
    ]
    for sensor in sensor_types:
        SensorType.objects.get_or_create(
            name=sensor["name"], description=sensor["description"], unit=sensor["unit"]
        )

def create_control_type(sender, **kwargs):
    control_types = [
        {"name": "light", "description": "Lampada LED Grow"},
        {"name": "pump", "description": "Compressor Aerador"}
    ]
    for control in control_types:
        ControlType.objects.get_or_create(name=control['name'],description=control['description'])