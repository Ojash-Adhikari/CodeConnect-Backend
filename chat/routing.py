from django.urls import path , include
from django.urls import re_path
from chat.consumers import MatchmakingConsumer

# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
    re_path(r'ws/chat/$', MatchmakingConsumer.as_asgi()),  
]