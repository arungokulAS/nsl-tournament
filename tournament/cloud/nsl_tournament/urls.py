
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("NSL TEST PLAIN RESPONSE")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]
