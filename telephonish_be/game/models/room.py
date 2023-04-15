from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    current_round_number = models.IntegerField(default=1)
