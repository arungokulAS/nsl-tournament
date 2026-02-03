
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
    path('groups/', views.groups_view, name='groups'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('live/', views.live_game_view, name='live'),
    path('', home, name='home'),
]
