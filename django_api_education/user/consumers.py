from channels.consumer import AsyncConsumer
import json
import aioredis


class UserConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print(self, event, " self.channel_name")
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data):
        data = json.loads(text_data.get("text"))
        event = data.get("event")
        user_id = data.get("userId")

        if event is None or user_id is None:
            await self.send_error("Event and userId are required fields")
            await self.close()

            return

        if event == "subscribe-on-new-car-in-shop":
            await self.subscribe_to_new_car_events(user_id)

    async def subscribe_to_new_car_events(self, user_id):
        print(type(self), "9998hhh")
        self.redis = await aioredis.from_url("redis://localhost")
        # await self.redis.set('new_car_subscribers', {'user_id': user_id, 'connection': self})
        await self.redis.sadd(
            "new_car_subscribers",
            json.dumps({"user_id": user_id, "connection": str(self)}),
        )
        self.redis.close()

    # async def send_message(self, data):
    #     text = json.dumps({"status": "success", "data": data})
    #     await self.send({
    #             "type": "websocket.send",
    #             "text": text
    #         })

    async def send_message(self, connection, data):
        text = json.dumps({"status": "success", "data": data})
        print(text, "kkk", connection)
        await connection.send({"type": "websocket.send", "text": text})

    async def send_error(self, message):
        await self.send(
            {"type": "websocket.send", "text": json.dumps({"error": message})}
        )

    async def close(self):
        await self.close()

    async def websocket_disconnect(self, event):
        self.redis = await aioredis.from_url("redis://localhost")
        await self.redis.delete("new_car_subscribers")
        self.redis.close()
        print("disconected", event)
