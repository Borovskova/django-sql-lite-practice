"""
ASGI config for django_api_education project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

import car.consumers
import user.consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_api_education.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/user", user.consumers.UserConsumer.as_asgi()),
                    path("ws/car", car.consumers.CarConsumer.as_asgi()),
                ]
            )
        ),
    }
)
