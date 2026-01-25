from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Team
from .forms import TeamForm
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'home.html')

def teams_list(request):
    teams = Team.objects.all()
    is_locked = teams.first().is_locked if teams.exists() else False
    return render(request, 'teams.html', {'teams': teams, 'is_locked': is_locked})

@require_POST
def add_team(request):
    if Team.objects.filter(is_locked=True).exists():
        messages.error(request, 'Teams are locked.')
        return redirect('teams')
    form = TeamForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Team added.')
    return redirect('teams')

@require_POST
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if team.is_locked:
        messages.error(request, 'Teams are locked.')
        return redirect('teams')
    form = TeamForm(request.POST, instance=team)
    if form.is_valid():
        form.save()
        messages.success(request, 'Team updated.')
    return redirect('teams')

@require_POST
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if team.is_locked:
        messages.error(request, 'Teams are locked.')
        return redirect('teams')
    team.delete()
    messages.success(request, 'Team deleted.')
    return redirect('teams')

@require_POST
def lock_teams(request):
    Team.objects.all().update(is_locked=True)
    messages.success(request, 'Teams locked.')
    return redirect('teams')
