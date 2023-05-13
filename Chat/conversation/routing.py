from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/private_chat/(?P<room_name>\w+)/(?P<other_user>\w+)/$', ChatConsumer.as_asgi()),
]