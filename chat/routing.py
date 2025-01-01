from django.urls import path , include
from django.urls import re_path
from chat.consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
    re_path(r'ws/chat/$', ChatConsumer.as_asgi()),  # Add this in routing.py or asgi.py
]