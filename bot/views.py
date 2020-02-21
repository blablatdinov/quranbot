from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import telebot
import random
from telebot import types
from quranbot.settings import DJANGO_TELEGRAMBOT
from billiard.pool import MaybeEncodingError

from .models import *


token = DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']
webhook_url = DJANGO_TELEGRAMBOT['WEBHOOK_SITE']
tbot = telebot.TeleBot(token)
tbot.remove_webhook()
tbot.set_webhook(f'{webhook_url}/{token}')


markup = types.ReplyKeyboardMarkup()
item = types.KeyboardButton('Подкасты')
markup.row(item)


def bot(request):
    print(3)
    if request.content_type == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        print(2)
        return HttpResponse('')

    else:
        raise PermissionDenied


@tbot.message_handler(commands=['start'])
def start_handler(message):
    print(1)
    try:
        s = Subscribers.objects.get(telegram_chat_id=message.chat.id)
        if s.status:
            tbot.send_message(message.chat.id, 'Вы уже зарегистрированы',
                              reply_markup=markup)
        else:
            s.status = True
            s.save()
            tbot.send_message(message.chat.id, f'Ваш статус "*Активен*", вы продолжите с дня {s.day}',
                              parse_mode='Markdown', reply_markup=markup)
    except:
        day_content = QuranOneDayContent.objects.get(day=1)
        subscriber = Subscribers(telegram_chat_id=message.chat.id, day=1)
        subscriber.save()
        tbot.send_message(message.chat.id, day_content.content_for_day(), parse_mode='Markdown', reply_markup=markup)




@tbot.message_handler(content_types=['text'])
def audio(message):
    if message.text == 'Подкасты':
        audio = Audio.objects.get(id=random.randint(1, 1866))
        if audio.tg_audio_link != '':
            tbot.send_audio(message.chat.id, audio.tg_audio_link)
        else:
            tbot.send_message(message.chat.id, audio.audio_link)

# @tbot.message_handler(commands=['audio'])
# def audio(message):

#     tbot.send_message(message.chat.id, "Choose one letter:")
