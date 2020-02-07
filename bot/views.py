from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot
from quranbot.settings import DJANGO_TELEGRAMBOT

from .models import *


token = DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']
tbot = telebot.TeleBot(token)
tbot.remove_webhook()
tbot.set_webhook('https://blablatdinov.ru/705810219:AAHwIwmLT7P3ffdP5fV6OFy2kWvBSDERGNk')


def bot(request):

    if request.content_type == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])

        return HttpResponse('')

    else:
        raise PermissionDenied


@tbot.message_handler(commands=['start'])
def start_handler(message):
    try:
        s = Subscribers.objects.get(telegram_chat_id=message.chat.id)
        content = QuranOneDayContent.objects.get(pk=1)
        tbot.send_message(message.chat.id, 'Вы уже зарегистрированы')
    except:
        day_content = QuranOneDayContent.objects.get(pk=1)
        subscriber = Subscribers(telegram_chat_id=message.chat.id)
        subscriber.save()
        day_content.subscribers.add(subscriber)
        tbot.send_message(message.chat.id, day_content.content)
