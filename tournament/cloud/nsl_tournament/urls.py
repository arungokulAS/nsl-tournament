from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teams/', views.teams_view, name='teams'),
    path('team-list/', views.team_list_view, name='team_list'),
    path('groups/', views.group_list_view, name='groups'),
    path('points/', views.points_table_view, name='points'),
    # Public results
    path('results/group-stage/', views.results_group_stage_view, name='results_group_stage'),
    path('results/qualifier/', views.results_qualifier_view, name='results_qualifier'),
    path('results/pre-quarter/', views.results_pre_quarter_view, name='results_pre_quarter'),
    path('results/knockout/', views.results_knockout_view, name='results_knockout'),
    path('contact/', views.contact_view, name='contact'),
    path('winners/', views.winners_view, name='winners'),
    # Admin routes (all under /tadmin/)
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('tadmin/teams/', views.admin_teams_view, name='admin_teams'),
    path('tadmin/groups/', views.admin_groups_view, name='admin_groups'),
    path('tadmin/groups-manage/', views.admin_groups_manage_view, name='admin_groups_manage'),
    path('tadmin/schedule/', views.admin_schedule_manage_view, name='admin_schedule_manage'),
    path('tadmin/schedule/group-stage/', views.admin_schedule_group_stage_view, name='admin_schedule_group_stage'),
    path('tadmin/schedule/qualifier/', views.admin_schedule_qualifier_view, name='admin_schedule_qualifier'),
    path('tadmin/live/', views.admin_live_manage_view, name='admin_live_manage'),
    path('tadmin/finish-rounds/', views.admin_finish_rounds_manage_view, name='admin_finish_rounds_manage'),
    path('tadmin/group-lock/', views.admin_group_lock_view, name='admin_group_lock'),
    path('tadmin/group-complete/', views.admin_group_complete_view, name='admin_group_complete'),
    path('tadmin/sponsors/', views.sponsors_details_view, name='sponsors_details'),
    # Referee
    path('referee/court/<int:court_id>/', views.referee_court_view, name='referee_court'),
    ]
