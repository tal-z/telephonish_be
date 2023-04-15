from django.db import models
from .round import RoundFormat


class Response(models.Model):
    round = models.ForeignKey('game.Round', on_delete=models.CASCADE)
    player = models.ForeignKey('game.Player', on_delete=models.CASCADE)
    preceding_prompt = models.ForeignKey('game.Prompt', on_delete=models.CASCADE)
    content = models.TextField()
    format = models.CharField(max_length=10, choices=RoundFormat.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
