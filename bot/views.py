from time import sleep

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import telebot
import random
from telebot import types
from quranbot.settings import DJANGO_TELEGRAMBOT
from billiard.pool import MaybeEncodingError

from .models import *

from .utils import save_message


token = DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']
webhook_url = DJANGO_TELEGRAMBOT['WEBHOOK_SITE']
tbot = telebot.TeleBot(token)
tbot.remove_webhook()
sleep(0.1)
tbot.set_webhook(f'{webhook_url}/{token}')


markup = types.ReplyKeyboardMarkup()
item = types.KeyboardButton('🎧Подкасты')
markup.row(item)


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
    save_message(message)
    try:
        s = Subscribers.objects.get(telegram_chat_id=message.chat.id)
        if s.status:
            msg = tbot.send_message(message.chat.id, 'Вы уже зарегистрированы',
                              reply_markup=markup)
            save_message(msg)
        else:
            s.status = True
            s.save()
            msg = tbot.send_message(message.chat.id, f'Ваш статус "*Активен*", вы продолжите с дня {s.day}',
                              parse_mode='Markdown', reply_markup=markup)
            save_message(msg)
    except:
        day_content = QuranOneDayContent.objects.get(day=1)
        subscriber = Subscribers(telegram_chat_id=message.chat.id, day=1)
        subscriber.save()
        msg = tbot.send_message(message.chat.id, day_content.content_for_day(), parse_mode='Markdown', reply_markup=markup)
        save_message(msg)


@tbot.message_handler(content_types=['text'])
def text(message):
    save_message(message)
    if message.text == '🎧Подкасты':
        audio = Audio.objects.get(id=random.randint(1, 1866))
        if audio.tg_audio_link != '':
            msg = tbot.send_audio(message.chat.id, audio.tg_audio_link, reply_markup=markup)
            save_message(msg)
        else:
            msg = tbot.send_message(message.chat.id, audio.audio_link, reply_markup=markup)
            save_message(msg)
    elif ':' in message.text:
        sa = QuranAyat.objects.get_ayat(message.text)
        print(type(sa))
        if type(sa) == str:
            msg = tbot.send_message(message.chat.id, sa, parse_mode='Markdown')
            save_message(msg)
        else:
            msg = tbot.send_message(message.chat.id, sa.get_content(), parse_mode='Markdown')
            save_message(msg)
            msg = tbot.send_audio(message.chat.id, sa.tg_audio_link)
            save_message(msg)
