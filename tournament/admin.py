from django.contrib import admin
from .models import Group, Team, Match


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'team_count')
    search_fields = ('name',)
    
    def team_count(self, obj):
        return obj.teams.count()
    team_count.short_description = 'Number of Teams'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'matches_played', 'matches_won', 'matches_lost', 'points')
    list_filter = ('group',)
    search_fields = ('name', 'players')
    readonly_fields = ('matches_played', 'matches_won', 'matches_lost', 'points')
    
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'group', 'players')
        }),
        ('Statistics', {
            'fields': ('matches_played', 'matches_won', 'matches_lost', 'points'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_teams', 'scheduled_time', 'status', 'score', 'venue')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('home_team__name', 'away_team__name', 'venue')
    date_hierarchy = 'scheduled_time'
    
    fieldsets = (
        ('Match Details', {
            'fields': ('home_team', 'away_team', 'scheduled_time', 'venue', 'status')
        }),
        ('Score', {
            'fields': ('home_score', 'away_score')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def match_teams(self, obj):
        return f"{obj.home_team} vs {obj.away_team}"
    match_teams.short_description = 'Match'
    
    def score(self, obj):
        return f"{obj.home_score} - {obj.away_score}"
    score.short_description = 'Score'
    
    def save_model(self, request, obj, form, change):
        """Update team stats when match status changes to completed"""
        super().save_model(request, obj, form, change)
        if obj.status == 'completed':
            obj.home_team.update_stats()
            obj.away_team.update_stats()
