from django.contrib import admin
from .models.player import Player
from .models.prompt import Prompt
from .models.response import Response
from .models.room import Room
from .models.round import Round


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'emoji', 'room', 'is_spectator')


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('round', 'player', 'content', 'format', 'timestamp')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('room', 'prompt', 'format', 'start_time', 'duration_in_seconds')
