import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("jjjj45")
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        if message:
            # Handle new message
            # For example, broadcast it to other users
            await self.channel_layer.group_send(
                "user_group", {"type": "user_message", "message": message}
            )

    async def user_message(self, event):
        message = event["message"]
        # Send the message to the client
        await self.send(text_data=json.dumps({"message": message}))
