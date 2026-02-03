from django.db import models
from django.utils import timezone

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    player1_name = models.CharField(max_length=100)
    player2_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name

class TeamsLock(models.Model):
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Teams Locked: {self.is_locked}"