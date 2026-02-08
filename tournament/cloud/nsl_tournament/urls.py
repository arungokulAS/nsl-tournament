    path('tadmin/groups-manage/', views.admin_groups_manage_view, name='admin_groups_manage'),
    path('tadmin/schedule/', views.admin_schedule_manage_view, name='admin_schedule_manage'),
    path('tadmin/live/', views.admin_live_manage_view, name='admin_live_manage'),
    path('tadmin/finish-rounds/', views.admin_finish_rounds_manage_view, name='admin_finish_rounds_manage'),
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
                path('contact/', views.contact_view, name='contact'),
            path('group-list/', views.group_list_view, name='group_list'),
            path('winners/', views.winners_view, name='winners'),
            path('points/', views.points_table_view, name='points'),
        path('results/group-stage', views.results_group_stage_view, name='results_group_stage'),
        path('results/qualifier', views.results_qualifier_view, name='results_qualifier'),
        path('results/pre-quarter', views.results_pre_quarter_view, name='results_pre_quarter'),
        path('results/knockout', views.results_knockout_view, name='results_knockout'),
    # path('admin/', admin.site.urls),  # Disabled default Django admin
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('referee/court/<int:court_id>/', views.referee_court_view, name='referee_court'),
    path('tadmin/teams/', views.admin_teams_view, name='admin_teams'),
    path('tadmin/groups/', views.admin_groups_view, name='admin_groups'),
    path('teams/', views.teams_view, name='teams'),
    path('team-list/', views.team_list_view, name='team_list'),
    path('groups/', views.group_list_view, name='groups'),
    path('schedule/', views.admin_schedule_group_stage_view, name='schedule'),
    path('live/', views.live_game_view, name='live'),
    path('results/', views.results_group_stage_view, name='results'),
    path('admin/schedule/group-stage', views.admin_schedule_group_stage_view, name='admin_schedule_group_stage'),
    path('admin/schedule/qualifier', views.admin_schedule_qualifier_view, name='admin_schedule_qualifier'),
    path('tadmin/sponsors/', views.sponsors_details_view, name='sponsors_details'),
    path('tadmin/group-lock/', views.admin_group_lock_view, name='admin_group_lock'),
    path('tadmin/group-complete/', views.admin_group_complete_view, name='admin_group_complete'),
    path('', home, name='home'),
]
