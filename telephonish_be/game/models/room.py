from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    current_round_number = models.IntegerField(default=1)
    one_sentence_story_round = models.BooleanField(null=True)
    drawing_round = models.BooleanField(null=True)
    poem_round = models.BooleanField(null=True)
    dramatic_reading_round = models.BooleanField(null=True)
    password = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Room ID: {self.id}; Room Name: {self.room_name}"
