# Move import to very top
from django.http import HttpRequest, HttpResponse
# --- Tournament Results View (placeholder, to be replaced with real logic) ---
def tournament_results_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'tournament_results.html')
# --- Tournament Live View (placeholder, to be replaced with real logic) ---
def tournament_live_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'tournament_live.html')
# --- Tournament Schedule View (placeholder, to be replaced with real logic) ---
def tournament_schedule_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'tournament_schedule.html')
# --- Tournament Groups View (placeholder, to be replaced with real logic) ---
def tournament_groups_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'tournament_groups.html')
# --- Tournament Teams View (placeholder, to be replaced with real logic) ---
    return render(request, 'tournament_live.html')
def tournament_teams_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'tournament_teams.html')
# --- Admin Schedule Pre-Quarter View (placeholder, to be replaced with real logic) ---
def admin_schedule_pre_quarter_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'tournament_schedule.html')
# --- Admin Schedule Group Stage View (placeholder, to be replaced with real logic) ---
def admin_schedule_group_stage_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('admin_schedule_group_stage_view placeholder')
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Team, TeamsLock
from django.utils import timezone
import csv
from io import TextIOWrapper
import os
from django.views.decorators.csrf import csrf_exempt

# --- Home View ---
def home(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    is_locked = lock_obj.is_locked
    return render(request, 'nsl_home.html', {'is_locked': is_locked})

# --- Admin Group Lock View ---
def admin_group_lock_view(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    locked = getattr(lock_obj, 'groups_locked', False)
    error = None
    if request.method == 'POST':
        password = request.POST.get('password')
        if password != ADMIN_PASSWORD:
            error = 'Incorrect admin password.'
        else:
            lock_obj.groups_locked = True
            lock_obj.save()
            locked = True
    return render(request, 'admin_group_lock.html', {'locked': locked, 'error': error})

# --- Admin Group Complete View ---
def admin_group_complete_view(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    completed = getattr(lock_obj, 'group_stage_finished', False)
    error = None
    # Enforce group stage can only be completed if groups are locked
    if not getattr(lock_obj, 'groups_locked', False):
        error = 'Cannot complete group stage before groups are locked.'
        return render(request, 'admin_group_complete.html', {'completed': completed, 'error': error})
    if request.method == 'POST':
        password = request.POST.get('password')
        if password != ADMIN_PASSWORD:
            error = 'Incorrect admin password.'
        else:
            lock_obj.group_stage_finished = True
            lock_obj.save()
            completed = True
    return render(request, 'admin_group_complete.html', {'completed': completed, 'error': error})

# --- New Admin Management Pages ---
def admin_groups_manage_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'admin_groups_manage.html')

def admin_schedule_manage_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'admin_schedule_manage.html')

def admin_live_manage_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'admin_live_manage.html')

def admin_finish_rounds_manage_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'admin_finish_rounds_manage.html')

# --- Admin Groups View ---
def admin_groups_view(request: HttpRequest) -> HttpResponse:
    teams = Team.objects.all()
    group_names = ['A', 'B', 'C', 'D', 'E', 'F']
    groups = []
    messages_list = []
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    if request.method == 'POST':
        action = request.POST.get('action')
        password = request.POST.get('password')
        if password != ADMIN_PASSWORD:
            messages_list.append('Incorrect admin password.')
        else:
            if action == 'manual_assign':
                for team in teams:
                    # TODO: Add manual assignment logic here
                    pass
            elif action == 'auto_assign':
                import random
                team_list = list(teams)
                random.shuffle(team_list)
                for idx, team in enumerate(team_list):
                    group = group_names[idx % len(group_names)]
                    team.group = group
                    team.save()
                messages_list.append('Teams auto-assigned to groups.')
            elif action == 'lock_groups':
                lock_obj.groups_locked = True
                lock_obj.save()
                messages_list.append('Groups locked. No further changes allowed.')
    for group in group_names:
        group_teams = [team.team_name for team in teams if getattr(team, 'group', None) == group]
        groups.append({'name': group, 'teams': group_teams})
    return render(request, 'admin_groups.html', {
        'teams': teams,
        'group_names': group_names,
        'groups_locked': getattr(lock_obj, 'groups_locked', False),
        'groups': groups,
        'messages': messages_list,
    })

# All imports at the top


# Constants
ADMIN_PASSWORD = "nsl2026"

def contact_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = f"Contact Form Submission from {name}"
        body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        try:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, ['netsmashersliverpool@gmail.com'])
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again later.')
    return render(request, 'contact.html')
def points_table_view(request: HttpRequest) -> HttpResponse:
    teams = list(Team.objects.all())
    # Add all required fields for the new point table, using default values if not present
    team_rows = []
    for team in teams:
        team_rows.append({
            'team_name': getattr(team, 'team_name', ''),
            'played': getattr(team, 'played', 0),
            'wins': getattr(team, 'wins', 0),
            'draws': getattr(team, 'draws', 0),
            'losses': getattr(team, 'losses', 0),
            'dif': getattr(team, 'dif', 0),
            'points': getattr(team, 'points', 0),
        })
    team_rows = sorted(team_rows, key=lambda t: t['points'], reverse=True)
    return render(request, 'points.html', {'teams': team_rows})
from django.http import HttpRequest, HttpResponse
def results_group_stage_view(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    group_stage_finished = getattr(lock_obj, 'group_stage_finished', False)
    group_names = ['A', 'B', 'C', 'D', 'E', 'F']
    teams = Team.objects.all()
    groups = []
    for group in group_names:
        group_teams = [team for team in teams if getattr(team, 'group', None) == group]
        group_table = []
        for idx, team in enumerate(group_teams):
            group_table.append({
                'rank': idx+1,
                'name': team.team_name,
                'points': getattr(team, 'points', 0),
                'qualified': group_stage_finished and idx < 4,
                'provisional': not group_stage_finished and idx < 4,
            })
        groups.append({'name': group, 'teams': group_table})
    return render(request, 'results_group_stage.html', {
        'groups': groups,
        'group_stage_finished': group_stage_finished,
    })

def results_qualifier_view(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    qualifier_finished = getattr(lock_obj, 'qualifier_finished', False)
    # Demo: blocks and teams
    blocks = [
        {'rank_range': '1-4', 'teams': [{'name': f'Team {i}', 'winner': i==1, 'eliminated': False} for i in range(1,5)]},
        {'rank_range': '5-8', 'teams': [{'name': f'Team {i}', 'winner': False, 'eliminated': False} for i in range(5,9)]},
        {'rank_range': '9-12', 'teams': [{'name': f'Team {i}', 'winner': False, 'eliminated': True} for i in range(9,13)]},
        {'rank_range': '13-16', 'teams': [{'name': f'Team {i}', 'winner': False, 'eliminated': True} for i in range(13,17)]},
    ]
    return render(request, 'results_qualifier.html', {
        'blocks': blocks,
        'qualifier_finished': qualifier_finished,
    })

def results_pre_quarter_view(request: HttpRequest) -> HttpResponse:
    matches = [
        {'name': 'Match 1', 'winner': 'Team 1', 'eliminated': 'Team 2'},
        {'name': 'Match 2', 'winner': 'Team 3', 'eliminated': 'Team 4'},
    ]
    return render(request, 'results_pre_quarter.html', {'matches': matches})

def results_knockout_view(request: HttpRequest) -> HttpResponse:
    matches = [
        {'bracket': 'Quarterfinal 1', 'winner': 'Team 1', 'eliminated': 'Team 2'},
        {'bracket': 'Quarterfinal 2', 'winner': 'Team 3', 'eliminated': 'Team 4'},
    ]
    return render(request, 'results_knockout.html', {'matches': matches})
from django.views.decorators.csrf import csrf_exempt

def referee_court_view(request: HttpRequest, court_id: int) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    round_completed = getattr(lock_obj, 'qualifier_finished', False)
    matches = getattr(lock_obj, 'qualifier_schedule', [])
    court_matches = []
    for match in matches:
        if str(match.get('court', '').replace('Court ', '')) == str(court_id):
            if match.get('status') in ['Scheduled', 'Active']:
                court_matches.append(match)
    if request.method == 'GET':
        return render(request, 'referee_court.html', {'court_id': court_id, 'court_matches': court_matches, 'round_completed': round_completed})
    # Score update logic
    if request.method == 'POST' and not round_completed:
        match_id = request.POST.get('match_id')
        score1 = request.POST.get('score1')
        score2 = request.POST.get('score2')
        for match in matches:
            if str(match.get('match_id', '')) == str(match_id):
                match['score1'] = int(score1)
                match['score2'] = int(score2)
                match['status'] = 'Active'  # Mark as active after score update
                # Lock row after match ends (simulate logic)
                if 'completed' in request.POST:
                    match['status'] = 'Completed'
        lock_obj.qualifier_schedule = matches
        lock_obj.save()
        # Update results, points, qualification logic here (stub)
        # ...
        return redirect(f'/referee/court/{court_id}/')
    # Add match_id for each row for demo
    for idx, match in enumerate(court_matches):
        match['match_id'] = idx
    # Mark locked if status is Completed
    for match in court_matches:
        match['locked'] = match.get('status') == 'Completed'
    return render(request, 'referee_court.html', {
        'court_id': court_id,
        'matches': court_matches,
        'round_completed': round_completed,
    })
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Team, TeamsLock
from django.utils import timezone
from django.contrib import messages
import csv
from io import TextIOWrapper
import os
from django.conf import settings

def admin_schedule_qualifier_view(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    prev_round_finished = getattr(lock_obj, 'group_stage_finished', False)
    schedule_locked = getattr(lock_obj, 'qualifier_schedule_locked', False)
    round_finished = getattr(lock_obj, 'qualifier_finished', False)
    schedule = getattr(lock_obj, 'qualifier_schedule', [])
    messages_list = []
    if not prev_round_finished:
        messages_list.append('Cannot schedule Qualifier until Group Stage is finished.')
        return render(request, 'admin_schedule_qualifier.html', {
            'schedule': [],
            'schedule_locked': False,
            'round_finished': False,
            'messages': messages_list,
        })
    if request.method == 'POST':
        action = request.POST.get('action')
        password = request.POST.get('password')
        if password != ADMIN_PASSWORD:
            messages_list.append('Incorrect admin password.')
        else:
            if action == 'generate_schedule' and not schedule_locked:
                court_count = int(request.POST.get('court_count', 4))
                group_names = ['A', 'B', 'C', 'D', 'E', 'F']
                teams = Team.objects.all()
                qualified = []
                for group in group_names:
                    group_teams = [team for team in teams if getattr(team, 'group', None) == group]
                    group_teams = sorted(group_teams, key=lambda t: getattr(t, 'points', 0), reverse=True)
                    qualified.extend([t.team_name for t in group_teams[:4]])
                matches = []
                for i in range(0, len(qualified), 2):
                    if i+1 < len(qualified):
                        matches.append({'match': f'{qualified[i]} vs {qualified[i+1]}'})
                for idx, match in enumerate(matches):
                    match['court'] = f'Court {idx % court_count + 1}'
                    match['status'] = 'Scheduled'
                lock_obj.qualifier_schedule = matches
                lock_obj.qualifier_schedule_locked = True
                lock_obj.save()
                schedule = matches
                messages_list.append('Qualifier schedule generated and locked.')
            elif action == 'delete_schedule' and not schedule_locked:
                lock_obj.qualifier_schedule = []
                lock_obj.save()
                schedule = []
                messages_list.append('Qualifier schedule deleted.')
            elif action == 'finish_round' and schedule_locked and not round_finished:
                for match in schedule:
                    match['status'] = 'Completed'
                lock_obj.qualifier_finished = True
                # Best loser logic: select 4 teams with highest points among non-qualifiers
                group_names = ['A', 'B', 'C', 'D', 'E', 'F']
                teams = Team.objects.all()
                qualified = set()
                for group in group_names:
                    group_teams = [team for team in teams if getattr(team, 'group', None) == group]
                    group_teams = sorted(group_teams, key=lambda t: getattr(t, 'points', 0), reverse=True)
                    qualified.update([t.team_name for t in group_teams[:4]])
                non_qualified = [t for t in teams if t.team_name not in qualified]
                best_losers = sorted(non_qualified, key=lambda t: getattr(t, 'points', 0), reverse=True)[:4]
                lock_obj.best_losers = [t.team_name for t in best_losers]
                lock_obj.save()
                round_finished = True
                messages_list.append('Qualifier finished, best losers selected, and archived.')
    return render(request, 'admin_schedule_qualifier.html', {
        'schedule': schedule,
        'schedule_locked': getattr(lock_obj, 'qualifier_schedule_locked', False),
        'round_finished': getattr(lock_obj, 'qualifier_finished', False),
        'messages': messages_list,
    })

# --- Admin Schedule Group Stage View ---
def group_list_view(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    is_locked = getattr(lock_obj, 'is_locked', False)
    group_names = ['A', 'B', 'C', 'D', 'E', 'F']
    teams = Team.objects.all()
    groups = []
    for group in group_names:
        group_teams = [team for team in teams if getattr(team, 'group', None) == group]
        groups.append({'name': group, 'teams': [t.team_name for t in group_teams]})
    return render(request, 'groups.html', {
        'groups': groups,
        'is_locked': is_locked,
    })

def winners_view(request: HttpRequest) -> HttpResponse:
    # For demo, assume teams with points > 0 are winners
    teams = Team.objects.all()
    winners = [team for team in teams if getattr(team, 'points', 0) > 0]
    return render(request, 'winners.html', {'winners': winners})

def points_table_view(request: HttpRequest) -> HttpResponse:
    from .models import Team
    teams = list(Team.objects.all())
    for team in teams:
        team.points = getattr(team, 'points', 0)
    teams = sorted(teams, key=lambda t: getattr(t, 'points', 0), reverse=True)
    return render(request, 'points.html', {'teams': teams})
    teams = Team.objects.all().order_by('created_at')
    groups = []
    messages_list = []
    if request.method == 'POST':
        action = request.POST.get('action')
        password = request.POST.get('password')
        if password != ADMIN_PASSWORD:
            messages_list.append('Incorrect admin password.')
        else:
            if action == 'manual_assign':
                # Manual assignment logic (store group for each team)
                for team in teams:
                    group = request.POST.get(f'group_{team.team_id}')
                    if group in group_names:
                        team.group = group
                        team.save()
                messages_list.append('Manual group assignment saved.')
            elif action == 'auto_assign':
                # Auto-random assignment logic
                import random
                team_list = list(teams)
                random.shuffle(team_list)
                for idx, team in enumerate(team_list):
                    group = group_names[idx % len(group_names)]
                    team.group = group
                    team.save()
                messages_list.append('Teams auto-assigned to groups.')
            elif action == 'lock_groups':
                lock_obj.groups_locked = True
                lock_obj.save()
                messages_list.append('Groups locked. No further changes allowed.')
    # Prepare groups for display
    for group in group_names:
        group_teams = [team.team_name for team in teams if getattr(team, 'group', None) == group]
        groups.append({'name': group, 'teams': group_teams})
    return render(request, 'admin_groups.html', {
        'teams': teams,
        'group_names': group_names,
        'groups_locked': getattr(lock_obj, 'groups_locked', False),
        'groups': groups,
        'messages': messages_list,
    })

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Team, TeamsLock
from django.utils import timezone
from django.contrib import messages
import csv
from io import TextIOWrapper
import os
from django.conf import settings

ADMIN_PASSWORD = "nsl2026"

def teams_view(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    is_locked = lock_obj.is_locked
    teams = Team.objects.all().order_by('created_at')
    return render(request, 'teams.html', {'teams': teams, 'is_locked': is_locked})

def team_list_view(request: HttpRequest) -> HttpResponse:
    teams = Team.objects.all().order_by('created_at')
    return render(request, 'team-list.html', {'teams': teams})

    # ...existing code...

def live_game_view(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    groups_locked = getattr(lock_obj, 'groups_locked', False)
    if not groups_locked:
        return render(request, 'live_game.html', {'live_games': [], 'groups_locked': False, 'message': 'Live game page is disabled until groups are locked.'})
    # Use frozen group data for live games
    group_names = ['A', 'B', 'C', 'D', 'E', 'F']
    teams = Team.objects.all()
    live_games = []
    for group in group_names:
        group_teams = [team.team_name for team in teams if getattr(team, 'group', None) == group]
        if group_teams:
            live_games.append({'match': f'{group_teams[0]} vs {group_teams[-1]}', 'score': 'TBD', 'status': 'Upcoming', 'group': group})
    return render(request, 'live_game.html', {'live_games': live_games, 'groups_locked': True})

def admin_teams_view(request: HttpRequest) -> HttpResponse:
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    is_locked = lock_obj.is_locked
    teams = Team.objects.all().order_by("created_at")
    edit_team = None

    if request.method == "POST":
        action = request.POST.get("action")
        password = request.POST.get("password")
        # Only require password for lock, edit, delete
        if action in ["lock", "edit", "delete"]:
            if password != ADMIN_PASSWORD:
                messages.error(request, "Incorrect admin password.")
                return redirect("/tadmin/teams/")

        if action == "lock":
            lock_obj.is_locked = True
            lock_obj.locked_at = timezone.now()
            lock_obj.save()
            messages.success(request, "Teams locked.")
            return redirect("/tadmin/teams/")

        if not is_locked:
            if action == "clear_all":
                if password != ADMIN_PASSWORD:
                    messages.error(request, "Incorrect admin password.")
                    return redirect("/teams/")
                Team.objects.all().delete()
                messages.success(request, "All teams cleared successfully.")
                return redirect("/teams/")
            if action == "upload_csv":
                csv_file = request.FILES.get("csv_file")
                if csv_file:
                    try:
                        reader = csv.reader(TextIOWrapper(csv_file, encoding="utf-8"))
                        first = True
                        added_count = 0
                        duplicate_count = 0
                        invalid_count = 0
                        for row in reader:
                            if first and ("player" in row[0].lower() or "name" in row[0].lower()):
                                first = False
                                continue
                            first = False
                            if len(row) < 2 or not row[0].strip() or not row[1].strip():
                                invalid_count += 1
                                continue
                            player1 = row[0].strip()
                            player2 = row[1].strip()
                            team_name = f"{player1} & {player2}"
                            if Team.objects.filter(team_name=team_name, player1_name=player1, player2_name=player2).exists():
                                duplicate_count += 1
                                continue
                            Team.objects.create(
                                team_name=team_name,
                                player1_name=player1,
                                player2_name=player2,
                            )
                            added_count += 1
                        if added_count > 0:
                            messages.success(request, f"{added_count} new teams added.")
                        if duplicate_count > 0:
                            messages.warning(request, f"{duplicate_count} duplicate teams skipped.")
                        if invalid_count > 0:
                            messages.error(request, f"{invalid_count} invalid rows skipped.")
                        if added_count == 0 and duplicate_count == 0 and invalid_count == 0:
                            messages.warning(request, "No valid teams found in file.")
                    except Exception as e:
                        messages.error(request, f"CSV upload failed: {e}")
                return redirect("/teams/")
            if action == "add":
                player1 = request.POST.get("player1_name")
                player2 = request.POST.get("player2_name")
                team_name = f"{player1} & {player2}"
                if Team.objects.filter(team_name=team_name, player1_name=player1, player2_name=player2).exists():
                    messages.error(request, "Duplicate team name. Team already exists.")
                else:
                    Team.objects.create(
                        team_name=team_name,
                        player1_name=player1,
                        player2_name=player2,
                    )
                    messages.success(request, "Team added.")
                return redirect("/tadmin/teams/")
            elif action == "edit":
                # If edit form submitted (with new names)
                if request.POST.get("player1_name") and request.POST.get("player2_name"):
                    team = Team.objects.get(team_id=request.POST.get("team_id"))
                    player1 = request.POST.get("player1_name")
                    player2 = request.POST.get("player2_name")
                    team.team_name = f"{player1} & {player2}"
                    team.player1_name = player1
                    team.player2_name = player2
                    team.save()
                    messages.success(request, "Team updated.")
                    return redirect("/tadmin/teams/")
                # Otherwise, show edit form for this team
                edit_team = Team.objects.get(team_id=request.POST.get("team_id"))
            elif action == "delete":
                team_id = request.POST.get("team_id")
                Team.objects.filter(team_id=team_id).delete()
                messages.success(request, "Team deleted.")
                return redirect("/tadmin/teams/")
    return render(request, "admin_teams.html", {
        "teams": teams,
        "is_locked": is_locked,
        "edit_team": edit_team,
    })

def sponsors_details_view(request):
    title_logo_url = None
    main_logo_url = None
    title_logo_path = os.path.join(settings.MEDIA_ROOT, 'title_sponsor.png')
    main_logo_path = os.path.join(settings.MEDIA_ROOT, 'main_sponsor.png')
    if os.path.exists(title_logo_path):
        title_logo_url = settings.MEDIA_URL + 'title_sponsor.png'
    if os.path.exists(main_logo_path):
        main_logo_url = settings.MEDIA_URL + 'main_sponsor.png'
    if request.method == 'POST':
        if request.POST.get('delete_logo') == 'title':
            if os.path.exists(title_logo_path):
                os.remove(title_logo_path)
            title_logo_url = None
        elif request.POST.get('delete_logo') == 'main':
            if os.path.exists(main_logo_path):
                os.remove(main_logo_path)
            main_logo_url = None
        else:
            if 'title_logo' in request.FILES:
                title_logo = request.FILES['title_logo']
                with open(title_logo_path, 'wb+') as f:
                    for chunk in title_logo.chunks():
                        f.write(chunk)
                title_logo_url = settings.MEDIA_URL + 'title_sponsor.png'
            if 'main_logo' in request.FILES:
                main_logo = request.FILES['main_logo']
                with open(main_logo_path, 'wb+') as f:
                    for chunk in main_logo.chunks():
                        f.write(chunk)
                main_logo_url = settings.MEDIA_URL + 'main_sponsor.png'
    return render(request, 'sponsors_details.html', {
        'title_logo_url': title_logo_url,
        'main_logo_url': main_logo_url,
    })

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'net smashers' and password == 'nsl123':
            request.session['is_admin'] = True
            return redirect('/tadmin/teams/')
        else:
            from django.contrib import messages
            messages.error(request, 'Invalid username or password.')
    return render(request, 'admin_login.html')
    # Restrict access to logged-in admins
    if not request.session.get('is_admin'):
        return redirect('/admin-login/')
