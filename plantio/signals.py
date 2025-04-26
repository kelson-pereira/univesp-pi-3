from .models import SensorType, ControlType


def create_sensor_type(sender, **kwargs):
    sensor_types = [
        {"name": "tmpA", "description": "Temperatura ambiente", "unit": "°C", "min_value": 20, "max_value": 32},
        {"name": "umdA", "description": "Umidade relativa do ar", "unit": "%", "min_value": 60, "max_value": 70},
        {"name": "tmpS", "description": "Temperatura da solução nutritiva", "unit": "°C", "min_value": 20, "max_value": 28},
        {"name": "levS", "description": "Nível da solução nutritiva", "unit": "", "min_value": 0.5, "max_value": 1.5},
    ]
    for sensor in sensor_types:
        SensorType.objects.get_or_create(
            name=sensor["name"], description=sensor["description"], unit=sensor["unit"], min_value=sensor["min_value"], max_value=sensor["max_value"]
        )

def create_control_type(sender, **kwargs):
    control_types = [
        {"name": "light", "description": "Lâmpada LED Grow"},
        {"name": "pump", "description": "Compressor Aerador"}
    ]
    for control in control_types:
        ControlType.objects.get_or_create(name=control['name'],description=control['description'])