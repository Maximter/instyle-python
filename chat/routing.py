from django.urls import re_path
from . import consumers
from django.urls import path


websocket_urlpatterns = [
    re_path(r"ws/socket-server/", consumers.ChatConsumer.as_asgi()),
]