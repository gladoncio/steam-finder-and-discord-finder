from django.urls import include, path
from rest_framework import routers
from .views import *

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
          path('steam-user/', SteamIDConverter.as_view(), name='steam-user'),
          path('discord-user/', DiscordUserView.as_view(), name='discord_user'),
]