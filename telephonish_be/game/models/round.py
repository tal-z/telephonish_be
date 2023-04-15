from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class RoundFormat(models.TextChoices):
    TEXT = 'text', _('Text')
    DRAWING = 'drawing', _('Drawing')
    EMOJI = 'emoji', _('Emoji')


class Round(models.Model):
    room = models.ForeignKey('game.Room', on_delete=models.CASCADE)
    prompt = models.ForeignKey('game.Prompt', on_delete=models.SET_NULL, null=True)
    format = models.CharField(max_length=255, choices=RoundFormat.choices)
    start_time = models.DateTimeField(default=timezone.now)
    duration_in_seconds = models.IntegerField()
