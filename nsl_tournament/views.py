from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Group, Team, GroupAssignment, Match, Court
from .forms import TeamForm, GroupAssignmentForm, ScheduleForm
from django.views.decorators.http import require_POST
from django.utils import timezone
import random

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

def groups_page(request):
    groups = Group.objects.all().order_by('name')
    teams = Team.objects.filter(is_locked=True)
    assignments = GroupAssignment.objects.select_related('team', 'group')
    is_locked = groups.first().is_locked if groups.exists() else False

    if request.method == "POST" and not is_locked:
        if "assign_manual" in request.POST:
            form = GroupAssignmentForm(request.POST)
            if form.is_valid():
                team = form.cleaned_data['team']
                group = form.cleaned_data['group']
                if not GroupAssignment.objects.filter(team=team).exists():
                    GroupAssignment.objects.create(team=team, group=group)
                    messages.success(request, "Team assigned to group.")
                else:
                    messages.error(request, "Team already assigned.")
            else:
                messages.error(request, "Invalid form.")
        elif "assign_auto" in request.POST:
            unassigned_teams = list(teams.exclude(id__in=assignments.values_list('team_id', flat=True)))
            group_list = list(groups)
            random.shuffle(unassigned_teams)
            for idx, team in enumerate(unassigned_teams):
                group = group_list[idx % len(group_list)]
                GroupAssignment.objects.create(team=team, group=group)
            messages.success(request, "Teams auto-assigned to groups.")
        elif "lock_groups" in request.POST:
            groups.update(is_locked=True)
            messages.success(request, "Groups locked.")

        return redirect('groups_page')

    form = GroupAssignmentForm()
    group_assignments = {g.name: [] for g in groups}
    for assignment in assignments:
        group_assignments[assignment.group.name].append(assignment.team)

    return render(request, "groups.html", {
        "groups": groups,
        "teams": teams,
        "form": form,
        "group_assignments": group_assignments,
        "is_locked": is_locked,
    })

def schedule_page(request, round_name):
    matches = Match.objects.filter(round_name=round_name).order_by('scheduled_time')
    is_locked = matches.first().is_locked if matches.exists() else False

    if request.method == "POST" and not is_locked:
        form = ScheduleForm(request.POST)
        if form.is_valid():
            num_courts = int(form.cleaned_data['num_courts'])
            start_time = form.cleaned_data['start_time']
            if round_name == 'group-stage':
                teams = list(Team.objects.filter(is_locked=True))
                random.shuffle(teams)
                courts = []
                for i in range(1, num_courts + 1):
                    court, _ = Court.objects.get_or_create(court_number=i)
                    courts.append(court)
                for i in range(0, len(teams), 2):
                    if i+1 < len(teams):
                        court = courts[(i//2) % num_courts]
                        Match.objects.create(
                            round_name=round_name,
                            team1=teams[i],
                            team2=teams[i+1],
                            court=court,
                            scheduled_time=start_time + timezone.timedelta(minutes=40*(i//(2*num_courts))),
                        )
                messages.success(request, "Schedule generated.")
        elif "lock_schedule" in request.POST:
            matches.update(is_locked=True)
            messages.success(request, "Schedule locked.")
        return redirect('schedule_page', round_name=round_name)

    form = ScheduleForm(initial={'round_name': round_name})
    courts = Court.objects.all().order_by('court_number')
    return render(request, "schedule.html", {
        "matches": matches,
        "form": form,
        "is_locked": is_locked,
        "courts": courts,
        "round_name": round_name,
    })
