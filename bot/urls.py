from django.urls import path
from quranbot.settings import DJANGO_TELEGRAMBOT
from bot.views import bot


token = DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']

urlpatterns = [
    path('705810219:AAHwIwmLT7P3ffdP5fV6OFy2kWvBSDERGNk', bot)
]