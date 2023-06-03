from django.contrib import admin
from django.utils.html import format_html
from .models.player import Player
from .models.prompt import Prompt
from .models.response import Response
from .models.room import Room
from .models.round import Round
from .models.drawing import Drawing
from .models.story import Story
from .models.poem import Poem


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'emoji', 'room', 'is_spectator')


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'room', 'round_number', 'display_dataurl')

    def display_dataurl(self, obj):
        return format_html('<img src="{}" width="100" height="100" />', obj.dataUrl)

    display_dataurl.short_description = 'Data URL'


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "room",
        "story",
    )


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = (
        "player",
        "room",
        "poem",
    )


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
