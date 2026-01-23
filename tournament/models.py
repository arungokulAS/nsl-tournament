from django.db import models
from django.utils import timezone


class Group(models.Model):
    """Model for tournament groups"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Team(models.Model):
    """Model for tournament teams"""
    name = models.CharField(max_length=200, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='teams')
    players = models.TextField(help_text="Enter player names separated by commas")
    
    # Stats
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    matches_lost = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-points', '-matches_won', 'name']
    
    def __str__(self):
        return self.name
    
    def update_stats(self):
        """Update team statistics based on matches"""
        home_matches = self.home_matches.filter(status='completed')
        away_matches = self.away_matches.filter(status='completed')
        
        matches_played = home_matches.count() + away_matches.count()
        matches_won = 0
        matches_lost = 0
        
        for match in home_matches:
            if match.home_score > match.away_score:
                matches_won += 1
            elif match.home_score < match.away_score:
                matches_lost += 1
        
        for match in away_matches:
            if match.away_score > match.home_score:
                matches_won += 1
            elif match.away_score < match.home_score:
                matches_lost += 1
        
        self.matches_played = matches_played
        self.matches_won = matches_won
        self.matches_lost = matches_lost
        self.points = matches_won * 3  # 3 points per win
        self.save()


class Match(models.Model):
    """Model for tournament matches"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('completed', 'Completed'),
    ]
    
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', db_index=True)
    
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    
    venue = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_time']
        verbose_name_plural = "Matches"
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.get_status_display()}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update team stats when match is completed
        if self.status == 'completed':
            self.home_team.update_stats()
            self.away_team.update_stats()
