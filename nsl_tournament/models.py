from django.db import models
from django.utils import timezone

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    player1_name = models.CharField(max_length=100)
    player2_name = models.CharField(max_length=100)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name

class Group(models.Model):
    GROUP_CHOICES = [
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('C', 'Group C'),
        ('D', 'Group D'),
        ('E', 'Group E'),
        ('F', 'Group F'),
    ]
    name = models.CharField(max_length=1, choices=GROUP_CHOICES, unique=True)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GroupAssignment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='assignments')
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_qualified = models.BooleanField(default=False)

    class Meta:
        unique_together = ('group', 'team')

class Court(models.Model):
    court_number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f'Court {self.court_number}'

class Match(models.Model):
    ROUND_CHOICES = [
        ('group-stage', 'Group Stage'),
        ('qualifier', 'Qualifier'),
        ('pre-quarter', 'Pre-Quarter'),
        ('quarter', 'Quarter'),
        ('semi', 'Semi'),
        ('final', 'Final'),
    ]
    round_name = models.CharField(max_length=20, choices=ROUND_CHOICES)
    team1 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team2_matches')
    court = models.ForeignKey(Court, on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_time = models.DateTimeField()
    is_locked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    winner = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.team1} vs {self.team2} ({self.round_name})'
