from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    #re_path(r'ws/chat/(?P<conversation_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]