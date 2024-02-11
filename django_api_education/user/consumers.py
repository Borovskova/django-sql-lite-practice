# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class UserConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print('hhhh')
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data.get('message')
#         if message:
#             # Handle new message
#             # For example, broadcast it to other users
#             await self.channel_layer.group_send(
#                 'user_group',
#                 {
#                     'type': 'user_message',
#                     'message': message
#                 }
#             )

#     async def user_message(self, event):
#         message = event['message']
#         # Send the message to the client
#         await self.send(text_data=json.dumps({'message': message}))

from channels.consumer import AsyncConsumer
import json
import aioredis

class UserConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print(self)
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data):
        data = json.loads(text_data.get('text'))
        event = data.get('event')
        user_id = data.get('userId')

        if event is None or user_id is None:
            await self.send_error("Event and userId are required fields")
            await self.close()

            return
        
        if event == 'subscribe-on-new-car-in-shop':
            await self.subscribe_to_new_car_events(user_id)
           
    async def subscribe_to_new_car_events(self, user_id):
        print(self, user_id, 'user_id')
        self.redis = await aioredis.from_url('redis://localhost')
        # await self.redis.set('new_car_subscribers', user_id)
        await self.redis.sadd('new_car_subscribers', user_id)
        self.redis.close()
    
    async def send_message(self, data):
        text = json.dumps({"status": "success", "data": data})
        await self.send({
                "type": "websocket.send",
                "text": text
            })
        
    async def send_error(self, message):
        await self.send({
            "type": "websocket.send",
            "text": json.dumps({"error": message})
        })

    async def close(self):
        await self.close()


    async def websocket_disconnect(self, event):
        self.redis = await aioredis.from_url('redis://localhost')
        await self.redis.delete('new_car_subscribers')
        self.redis.close()

    async def get_user_connection(self, scope, user_id):
        print(self, user_id)
        connection = await self.redis.get(user_id)
        return connection.decode('utf-8') if connection else None
    