import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LedControlConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "led_control"

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

    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data['status']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'led_status_update',
                'status': status
            }
        )

    async def led_status_update(self, event):
        await self.send(text_data=json.dumps({
            'status': event['status']
        }))
