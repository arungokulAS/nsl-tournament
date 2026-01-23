from django.urls import path
from . import views

app_name = 'tournament'

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('live/', views.live_games, name='live_games'),
    path('live/data/', views.live_games_data, name='live_games_data'),
    path('table/', views.point_table, name='point_table'),
    path('table/data/', views.point_table_data, name='point_table_data'),
    path('results/', views.results, name='results'),
]
