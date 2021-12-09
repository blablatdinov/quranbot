from django.conf import settings
from django.urls import path

from apps.bot_init.views import bot

urlpatterns = [
    path(f"{settings.TG_BOT.token}", bot),
]
