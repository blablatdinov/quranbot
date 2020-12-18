from django.urls import path

from django.conf import settings
from bot_init.views import bot


urlpatterns = [
    path(f"{settings.TG_BOT.token}", bot)
]
