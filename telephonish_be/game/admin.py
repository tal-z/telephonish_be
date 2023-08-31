from django.contrib import admin
from django.utils.html import format_html
from .models.player import Player
from .models.room import Room
from .models.drawing import Drawing
from .models.story import Story
from .models.poem import Poem


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'emoji', 'room', 'is_spectator')


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ('id', 'player_name', 'room', 'round_number', 'display_dataurl')

    def display_dataurl(self, obj):
        return format_html('<img src="{}" width="100" height="100" />', obj.dataUrl)

    display_dataurl.short_description = 'Data URL'

    def player_name(self, obj):
        return obj.player.name

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        "player_name",
        "room",
        "round_number",
        "story",
    )

    def player_name(self, obj):
        return obj.player.name


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        "player_name",
        "room",
        "round_number",
        "poem",
    )

    def player_name(self, obj):
        return obj.player.name



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

