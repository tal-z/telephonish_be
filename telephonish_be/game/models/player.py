from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=1)
    room = models.ForeignKey('game.Room', on_delete=models.CASCADE, related_name='players')
    is_spectator = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'room'], name='unique_spectator_name_in_room')
        ]
