from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Group, Team, Match


def home(request):
    """Home page showing tournament overview"""
    context = {
        'total_teams': Team.objects.count(),
        'total_groups': Group.objects.count(),
        'upcoming_matches': Match.objects.filter(status='scheduled').count(),
        'live_matches': Match.objects.filter(status='live').count(),
    }
    return render(request, 'tournament/home.html', context)


def schedule(request):
    """Show scheduled matches"""
    matches = Match.objects.filter(status='scheduled').select_related('home_team', 'away_team')
    return render(request, 'tournament/schedule.html', {'matches': matches})


def live_games(request):
    """Show live matches"""
    matches = Match.objects.filter(status='live').select_related('home_team', 'away_team')
    return render(request, 'tournament/live_games.html', {'matches': matches})


def live_games_data(request):
    """API endpoint for live game data (for AJAX refresh)"""
    matches = Match.objects.filter(status='live').select_related('home_team', 'away_team')
    data = [{
        'id': match.id,
        'home_team': match.home_team.name,
        'away_team': match.away_team.name,
        'home_score': match.home_score,
        'away_score': match.away_score,
        'venue': match.venue,
    } for match in matches]
    return JsonResponse({'matches': data})


def point_table(request):
    """Show point table/standings"""
    groups = Group.objects.prefetch_related('teams').all()
    return render(request, 'tournament/point_table.html', {'groups': groups})


def point_table_data(request):
    """API endpoint for point table data (for AJAX refresh)"""
    groups_data = []
    for group in Group.objects.prefetch_related('teams').all():
        teams_data = [{
            'name': team.name,
            'played': team.matches_played,
            'won': team.matches_won,
            'lost': team.matches_lost,
            'points': team.points,
        } for team in group.teams.all()]
        groups_data.append({
            'name': group.name,
            'teams': teams_data
        })
    return JsonResponse({'groups': groups_data})


def results(request):
    """Show completed matches/results"""
    matches = Match.objects.filter(status='completed').select_related('home_team', 'away_team').order_by('-scheduled_time')
    return render(request, 'tournament/results.html', {'matches': matches})
