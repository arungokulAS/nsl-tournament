from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from . import views

def home(request):
    from .models import TeamsLock
    lock_obj, _ = TeamsLock.objects.get_or_create(pk=1)
    is_locked = lock_obj.is_locked
    return render(request, 'nsl_home.html', {'is_locked': is_locked})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('tadmin/teams/', views.admin_teams_view, name='admin_teams'),
    path('tadmin/groups/', views.admin_groups_view, name='admin_groups'),
    path('teams/', views.teams_view, name='teams'),
    path('team-list/', views.team_list_view, name='team_list'),
    path('groups/', views.groups_view, name='groups'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('live/', views.live_game_view, name='live'),
        path('results/', views.results_view, name='results'),
    path('tadmin/sponsors/', views.sponsors_details_view, name='sponsors_details'),
    path('', home, name='home'),
]
