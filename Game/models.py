from django.db import models
from datetime import datetime

class Game (models.Model):
    redScore = models.IntegerField()
    blueScore = models.IntegerField()
    master = models.IntegerField()
    date = models.DateTimeField(default = datetime.now)
    
class GameInfo(models.Model):
    gameID = models.IntegerField()
    playerID = models.IntegerField()
    team = models.IntegerField()
    name = models.CharField(max_length=100, default = "")
    level = models.IntegerField(default = 0)
