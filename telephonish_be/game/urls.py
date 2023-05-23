from django.urls import path
from .views.room_views import (
    RoomCreateView,
    # RoomJoinView,
    GetRoomDataView,
    CheckPasswordRequirementView,
)

urlpatterns = [
    path('create-room/', RoomCreateView.as_view()),
    # path('join-room/', RoomJoinView.as_view()),
    path('get-room-info/<str:room_name>', GetRoomDataView.as_view()),
    path('get-password-requirement/<str:room_name>', CheckPasswordRequirementView.as_view()),
]