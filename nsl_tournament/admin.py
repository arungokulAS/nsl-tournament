from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'team_name', 'player1_name', 'player2_name', 'is_locked', 'created_at', 'updated_at')
    list_editable = ('team_name', 'player1_name', 'player2_name')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('team_name', 'player1_name', 'player2_name')
