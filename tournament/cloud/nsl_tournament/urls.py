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
    # Admin routes (all under /admin/)
    path('admin/login/', views.admin_login_view, name='admin_login'),
    path('admin/teams/', views.admin_teams_view, name='admin_teams'),
    path('admin/groups/', views.admin_groups_view, name='admin_groups'),
    path('admin/group-lock/', views.admin_group_lock_view, name='admin_group_lock'),
    path('admin/group-complete/', views.admin_group_complete_view, name='admin_group_complete'),
    path('admin/schedule/group-stage/', views.admin_schedule_group_stage_view, name='admin_schedule_group_stage'),
    path('admin/schedule/qualifier/', views.admin_schedule_qualifier_view, name='admin_schedule_qualifier'),
    path('admin/schedule/pre-quarter/', views.admin_schedule_pre_quarter_view, name='admin_schedule_pre_quarter'),
    path('admin/live-manage/', views.admin_live_manage_view, name='admin_live_manage'),
    path('admin/finish-round/', views.admin_finish_rounds_manage_view, name='admin_finish_rounds_manage'),
    # Referee
    path('referee/court/<int:court_id>/', views.referee_court_view, name='referee_court'),
    # Tournament (public, read-only)
    path('tournament/teams/', views.tournament_teams_view, name='tournament_teams'),
    path('tournament/groups/', views.tournament_groups_view, name='tournament_groups'),
    path('tournament/schedule/', views.tournament_schedule_view, name='tournament_schedule'),
    path('tournament/live/', views.tournament_live_view, name='tournament_live'),
    path('tournament/results/', views.tournament_results_view, name='tournament_results'),
    path('admin/sponsors/', views.sponsors_details_view, name='sponsors_details'),
]
