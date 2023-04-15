from django.urls import path
from .views import RoomCreateView

urlpatterns = [
    path('create-room/', RoomCreateView.as_view()),
]