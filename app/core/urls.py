from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import include
from .forms import *
from .views import *


urlpatterns = [
    path('', views.index, name='index'),
]