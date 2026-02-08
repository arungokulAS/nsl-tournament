
from django.db import models
from django.utils import timezone

# TeamsLock model for admin locking
class TeamsLock(models.Model):
    is_locked = models.BooleanField(default=False)
    groups_locked = models.BooleanField(default=False)
    def __str__(self):
        return f"TeamsLock (locked={self.is_locked}, groups_locked={self.groups_locked})"

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    player1_name = models.CharField(max_length=100)
    player2_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name


# Group model: round-1 grouping
class Group(models.Model):
    name = models.CharField(max_length=10)
    teams = models.ManyToManyField(Team, related_name='groups')
    locked = models.BooleanField(default=False)
    def __str__(self):
        return f"Group {self.name}"

# Schedule model: round-level container
class Schedule(models.Model):
    round_name = models.CharField(max_length=32)
    created_at = models.DateTimeField(default=timezone.now)
    locked = models.BooleanField(default=False)
    def __str__(self):
        return f"Schedule: {self.round_name}"

# Match model: individual matches
class Match(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='matches')
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team2')
    court = models.IntegerField()
    slot = models.IntegerField()
    round_name = models.CharField(max_length=32)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.round_name}: {self.team1} vs {self.team2}"

# Score model: score & outcome data
class Score(models.Model):
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='score')
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    winner = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_matches')
    point_difference = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Score: {self.match}"