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
        sura = int(message.text.split(':')[0])
        if 1 > sura > 114:
            msg = tbot.send_message(message.chat.id, 'Сура не найдена', reply_markup=markup)
            save_message(msg)
            return False
        ayat = int(message.text.split(':')[1])
        sura_ayats = QuranAyat.objects.filter(sura=sura)
        for sa in sura_ayats:
            sa_str = sa.__str__()
            sa_str_ayats = sa_str.split(':')[1]
            if '-' in sa_str:
                first_range_ayat = int(sa_str_ayats.split('-')[0])
                second_range_ayat = int(sa_str_ayats.split('-')[1])
                if ayat in range(first_range_ayat, second_range_ayat + 1):
                    msg = tbot.send_message(message.chat.id, sa.get_content(), parse_mode='Markdown', reply_markup=markup)
                    save_message(msg)
                    msg = tbot.send_audio(message.chat.id, sa.tg_audio_link, title=f'{sa.sura}:{sa.ayat}', performer='umma.ru')
                    save_message(msg)
                    print(sa_str)
                    return True
            elif ',' in sa_str_ayats:
                s = [int(x) for x in sa_str_ayats.split(',')]
                if ayat in s:
                    print(s)
                    msg = tbot.send_message(message.chat.id, sa.get_content(), parse_mode='Markdown')
                    save_message(msg)
                    msg = tbot.send_audio(message.chat.id, sa.tg_audio_link, title=f'{sa.sura}:{sa.ayat}', performer='umma.ru')
                    save_message(msg)
                    return True
            elif int(sa.ayat) == ayat:
                msg = tbot.send_message(message.chat.id, sa.get_content(), parse_mode='Markdown', reply_markup=markup)
                save_message(msg)
                msg = tbot.send_audio(message.chat.id, sa.tg_audio_link, title=f'{sa.sura}:{sa.ayat}', performer='umma.ru')
                save_message(msg)
                return True
        msg = tbot.send_message(message.chat.id, 'Аят не найден', reply_markup=markup)
        save_message(msg)
        return False
