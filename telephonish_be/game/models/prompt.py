from django.db import models


class Prompt(models.Model):
    text = models.TextField()
    preceding_response = models.ForeignKey('game.Response', blank=True, on_delete=models.CASCADE)

