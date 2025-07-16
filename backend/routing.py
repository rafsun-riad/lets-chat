from channels.routing import URLRouter
from django.urls import path

from chat_server.routing import websocket_urlpatterns as chat_websocket_urlpatterns

websocket_urlpatterns = [
    path(
        "ws/", URLRouter(chat_websocket_urlpatterns)
    ),  # for multiple websocket connections URLRouter([chat_websocket_urlpatterns, ...])
]
