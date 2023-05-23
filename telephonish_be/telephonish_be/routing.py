from django.urls import re_path
from telephonish_be.game import consumers

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<room_id>\w+)/(?P<username>\w+)/(?P<room_password>\w+)?/$", consumers.GameRoomConsumer.as_asgi()),
    re_path(r"ws/game/(?P<room_id>\w+)/(?P<username>\w+)/$",
            consumers.GameRoomConsumer.as_asgi()),

]