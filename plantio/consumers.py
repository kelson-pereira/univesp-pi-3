import json
from channels.generic.websocket import AsyncWebsocketConsumer


class LedControlConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "led_control"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data["status"]

        await self.channel_layer.group_send(
            self.group_name, {"type": "led_status_update", "status": status}
        )

    async def led_status_update(self, event):
        await self.send(text_data=json.dumps({"status": event["status"]}))


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_mac = self.scope['url_route']['kwargs']['device_mac']
        self.group_name = f'dashboard_{self.device_mac}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def device_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'device_update',
            'updated_now': event['updated_now'],
            'updated_at': event['updated_at']
        }))

    async def sensor_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'sensor_update',
            'sensor_type': event['sensor_type'],
            'value': event['value'],
            'status': event['status']
        }))

    async def control_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'control_update',
            'control_type': event['control_type'],
            'schedule_enabled': event['schedule_enabled'],
            'status': event['status']
        }))