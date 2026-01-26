
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

def home(request):
    print('Home view called')
    return render(request, 'nsl_home.html')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]
