from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Team, TeamsLock
from django.utils import timezone
from django.contrib import messages
import csv
from io import TextIOWrapper
import os
from django.conf import settings

ADMIN_PASSWORD = "nsl2026"

def teams_view(request: HttpRequest) -> HttpResponse:
    from django.contrib import messages as django_messages
    from .models import TeamsLock
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    is_locked = lock_obj.is_locked
    teams = Team.objects.all().order_by('created_at')
    return render(request, 'teams.html', {'teams': teams, 'messages': django_messages.get_messages(request), 'is_locked': is_locked})

def team_list_view(request: HttpRequest) -> HttpResponse:
    teams = Team.objects.all().order_by('created_at')
    return render(request, 'team-list.html', {'teams': teams})

def groups_view(request: HttpRequest) -> HttpResponse:
    from .models import TeamsLock
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    is_locked = lock_obj.is_locked
    groups = [
        {'name': 'Group 1', 'teams': ['Team A', 'Team C']},
        {'name': 'Group 2', 'teams': ['Team B', 'Team D']},
    ]
    return render(request, 'groups.html', {'groups': groups, 'is_locked': is_locked})

def schedule_view(request: HttpRequest) -> HttpResponse:
    # Replace with real data/model
    schedule = [
        {'match': 'Team A vs Team B', 'time': '2026-02-10 18:00'},
        {'match': 'Team C vs Team D', 'time': '2026-02-11 20:00'},
    ]
    return render(request, 'schedule.html', {'schedule': schedule})

def live_game_view(request: HttpRequest) -> HttpResponse:
    # Replace with real data/model
    live_games = [
        {'match': 'Team A vs Team B', 'score': '2-1', 'status': 'Live'},
    ]
    return render(request, 'live_game.html', {'live_games': live_games})

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
                        for row in reader:
                            if first and ("player" in row[0].lower() or "name" in row[0].lower()):
                                first = False
                                continue
                            first = False
                            if len(row) >= 2:
                                player1 = row[0].strip()
                                player2 = row[1].strip()
                                team_name = f"{player1} & {player2}"
                                if not Team.objects.filter(team_name=team_name, player1_name=player1, player2_name=player2).exists():
                                    Team.objects.create(
                                        team_name=team_name,
                                        player1_name=player1,
                                        player2_name=player2,
                                    )
                                    added_count += 1
                        if added_count > 0:
                            messages.success(request, "File Uploaded Successfully")
                        else:
                            messages.warning(request, "No new teams added. All teams already exist.")
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
        # Add authentication logic here
        # For now, just redirect to admin panel
        return redirect('/admin/')
    return render(request, 'admin_login.html')
