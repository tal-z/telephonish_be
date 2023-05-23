from django.db import models
from django.contrib.auth.hashers import make_password


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    current_round_number = models.IntegerField(default=0)
    one_sentence_story_round = models.BooleanField(null=True)
    drawing_round = models.BooleanField(null=True)
    poem_round = models.BooleanField(null=True)
    dramatic_reading_round = models.BooleanField(null=True)
    password = models.CharField(max_length=100, null=True, blank=True)

    @property
    def password_required(self):
        if self.password:
            return True
        return False

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return self.password_required and make_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Room ID: {self.id}; Room Name: {self.room_name}"