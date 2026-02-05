from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from . import views

def home(request):
    return render(request, 'nsl_home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tadmin/teams/', views.admin_teams_view, name='admin_teams'),
    path('teams/', views.teams_view, name='teams'),
    path('team-list/', views.team_list_view, name='team_list'),
    path('groups/', views.groups_view, name='groups'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('live/', views.live_game_view, name='live'),
    path('tadmin/sponsors/', views.sponsors_details_view, name='sponsors_details'),
    path('', home, name='home'),
]
