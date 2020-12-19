from django.urls import path

from django.conf import settings
from apps.bot_init.views import bot


urlpatterns = [
    path(f"{settings.TG_BOT.token}", bot)
]
