from django.db import models
from telephonish_be.game.models.player import Player
from telephonish_be.game.models.room import Room


class Poem(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    poem = models.TextField()
