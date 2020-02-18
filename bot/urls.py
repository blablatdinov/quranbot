from django.urls import path
from quranbot.settings import DJANGO_TELEGRAMBOT
from bot.views import bot


token = DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']

urlpatterns = [
    path(f'{token}', bot)
]
