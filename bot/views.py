from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot
from telebot import types
from quranbot.settings import DJANGO_TELEGRAMBOT

from .models import *


token = DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']
webhook_url = DJANGO_TELEGRAMBOT['WEBHOOK_SITE']
print(token)
tbot = telebot.TeleBot(token)
tbot.remove_webhook()
tbot.set_webhook(f'{webhook_url}/{token}')
print(f'{webhook_url}/{token}')


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
        if s.status:
            tbot.send_message(message.chat.id, 'Вы уже зарегистрированы')
        else:
            s.status = True
            s.save()
            tbot.send_message(message.chat.id, f'Ваш статус "*Активен*", вы продолжите с дня {s.day}',
                              parse_mode='Markdown')
    except:
        day_content = QuranOneDayContent.objects.get(day=1)
        subscriber = Subscribers(telegram_chat_id=message.chat.id, day=1)
        subscriber.save()
        tbot.send_message(message.chat.id, day_content.content)


# @tbot.message_handler(commands=['audio'])
# def audio(message):
#     markup = types.ReplyKeyboardMarkup()
#     item = types.KeyboardButton('/start')
#     markup.row(item)
#     tbot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)
