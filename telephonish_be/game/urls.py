from django.urls import path
from .views.room_views import (
    RoomCreateView,
    GetRoomDataView,
    GenerateRoomNameView,
    GeneratePlayerNameView,
    CheckPasswordRequirementView,
    GetGameplayDataView,
)
from .views.prompt_views import (
    SubmitStoryView,
    SubmitPoemView,
    SubmitDrawingView,
    GetStoryView,
    GetDrawingView,
    GetPoemView
)


urlpatterns = [
    # GET
    path('get-room-info/<str:room_name>', GetRoomDataView.as_view()),
    path('get-gameplay-info/<str:room_name>', GetGameplayDataView.as_view()),
    path('get-password-requirement/<str:room_name>', CheckPasswordRequirementView.as_view()),
    path('get-story/', GetStoryView.as_view(), name='get_story'),
    path('get-drawing/', GetDrawingView.as_view(), name='get_drawing'),
    path('get-poem/', GetPoemView.as_view(), name='get_drawing'),
    path('generate-room-name', GenerateRoomNameView.as_view()),
    path('generate-player-name', GeneratePlayerNameView.as_view()),
    # POST
    path('create-room/', RoomCreateView.as_view()),
    path('submit-story/', SubmitStoryView.as_view(), name='submit_story'),
    path('submit-poem/', SubmitPoemView.as_view(), name='submit_poem'),
    path('submit-drawing/', SubmitDrawingView.as_view(), name='submit_drawing'),
]
