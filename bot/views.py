# Импорт стандартных модулей python
from time import sleep
import random
# Импорт данных из настроек
from quranbot.settings import DEBUG
from quranbot.settings import DJANGO_TELEGRAMBOT
# Импорт доп. библиотек 
import telebot
from telebot import types
# Импорт модулей django
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from .models import *

from .utils import save_message


if DEBUG:
    r = telebot.apihelper.proxy = {'https': 'socks5://sockduser:ehodof21@66.55.70.132:7777'}
token = DJANGO_TELEGRAMBOT['BOTS'][0]['TOKEN']
webhook_url = DJANGO_TELEGRAMBOT['WEBHOOK_SITE']
tbot = telebot.TeleBot(token)
tbot.remove_webhook()
sleep(0.1)
tbot.set_webhook(f'{webhook_url}/{token}')


markup = types.ReplyKeyboardMarkup()
item = types.KeyboardButton('🎧Подкасты')
markup.row(item)
item = types.KeyboardButton('🌟Избранное')
markup.row(item)


def bot(request):
    if request.content_type == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        return HttpResponse('')

    else:
        raise PermissionDenied


@tbot.message_handler(commands=['start'])  # Обработчик команды старт
def start_handler(message):
    save_message(message)
    try:  # Если пользователь уже есть в нашей базе выполняется следующий код 
        s = Subscribers.objects.get(telegram_chat_id=message.chat.id)
        if s.status:
            msg = tbot.send_message(message.chat.id, 'Вы уже зарегистрированы',
                              reply_markup=markup)
            save_message(msg)
        else:
            s.status = True
            s.save()
            msg = tbot.send_message(message.chat.id, f'Ваш статус "<b>Активен</b>", вы продолжите с дня {s.day}',
                              parse_mode='HTML', reply_markup=markup)
            save_message(msg)
    except:  # Если пользователь отправил команду /start впервые
        start_mes = AdminMessage.objects.get(key='help').text
        msg = tbot.send_message(message.chat.id, start_mes, parse_mode='HTML')
        save_message(msg)
        day_content = QuranOneDayContent.objects.get(day=1)
        subscriber = Subscribers(telegram_chat_id=message.chat.id, day=1)
        subscriber.save()
        msg = tbot.send_message(message.chat.id, day_content.content_for_day(), parse_mode='HTML', reply_markup=markup)
        save_message(msg)
        msg = tbot.send_message(358610865, 'Зарегестрировался новый пользователь')
        save_message(msg)


@tbot.message_handler(commands=['help'])
def help_handler(message):
    save_message(message)
    help_mes = AdminMessage.objects.get(key='help').text
    msg = tbot.send_message(message.chat.id, help_mes, parse_mode='HTML', reply_markup=markup)
    save_message(msg)


@tbot.message_handler(commands=['dev'])  # Обработчик команды /dev
def to_dev(message):
    text = f'<b>Сообщение для разработчика:</b>\n\n{message.text[4:]}'
    msg = tbot.send_message(358610865, text, parse_mode='HTML')


def add_to_favorit(chat_id, ayat_pk):
    sub = Subscribers.objects.get(telegram_chat_id=int(chat_id))
    ayat = QuranAyat.objects.get(pk=ayat_pk)
    sub.favorit_ayats.add(ayat)


def send_ayats(tg_id, text):
    sa = QuranAyat.objects.get_ayat(text)
    #print(sa.pk)
    if type(sa) == str:
        msg = tbot.send_message(tg_id, sa, parse_mode='HTML')
        save_message(msg)
    else:
        keyboard = types.InlineKeyboardMarkup()
        if sa.pk == 1:
            next_ayat = QuranAyat.objects.get(pk=sa.pk+1)
            button =types.InlineKeyboardButton(text=next_ayat.__str__(), callback_data=next_ayat.__str__())
            keyboard.add(button)
            msg = tbot.send_message(tg_id, sa.get_content(), parse_mode='HTML', reply_markup=keyboard)
            save_message(msg)
            return ''
        if sa.pk == 5737:
            pres_ayat = QuranAyat.objects.get(pk=sa.pk-1)
            button =types.InlineKeyboardButton(text=pres_ayat.__str__(), callback_data=pres_ayat.__str__())
            keyboard.add(button)
            msg = tbot.send_message(tg_id, sa.get_content(), parse_mode='HTML', reply_markup=keyboard)
            save_message(msg)
            return ''

        pres_ayat = QuranAyat.objects.get(pk=sa.pk-1)
        next_ayat = QuranAyat.objects.get(pk=sa.pk+1)
        first_button = types.InlineKeyboardButton(text=pres_ayat.__str__(), callback_data=pres_ayat.__str__())
        second_button = types.InlineKeyboardButton(text=next_ayat.__str__(), callback_data=next_ayat.__str__())
        add_to_favorit_btn = types.InlineKeyboardButton(text='Добавить в избранное', callback_data=f'addToFav:pk={sa.pk}')
        keyboard.add(first_button, second_button)
        keyboard.add(add_to_favorit_btn)

        msg = tbot.send_message(tg_id, sa.get_content(), parse_mode='HTML', reply_markup=keyboard)
        save_message(msg)
        msg = tbot.send_audio(tg_id, sa.tg_audio_link)
        save_message(msg)


@tbot.message_handler(content_types=['text'])  # обработчик всех текстовых сообщений
def text(message):
    save_message(message)
    if message.text == 'подкасты' or message.text == 'Подкасты' or message.text == '🎧Подкасты':
        audio = random.choice(Audio.objects.all())
        if audio.tg_audio_link == '':
            msg = tbot.send_message(message.chat.id, audio.audio_link, reply_markup=markup)
        else:
            msg = tbot.send_audio(message.chat.id, audio.tg_audio_link, reply_markup=markup, performer='Шамиль Аляутдинов')
        save_message(msg)
    elif 'Избранное' in message.text:
        s = Subscribers.objects.get(telegram_chat_id=message.chat.id)
        ayats = s.favorit_ayats.all()
        response = ''
        for a in ayats:
            response += f'{a.sura}:{a.ayat}\n'
        msg = tbot.send_message(message.chat.id, response, reply_markup=markup)
        save_message(msg)
    elif ':' in message.text:
        send_ayats(message.chat.id, message.text)


@tbot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    import re
    chat_id = call.from_user.id
    text = call.data
    if 'addToFav' in text:
        ayat_pk = int(text[12:])
        add_to_favorit(chat_id, ayat_pk)
    else:
        regexp = r':\d+'
        sura = text.split(':')[0]
        ayats_range = text[text.find(':'):]
        ayat_with_colon = re.match(regexp, ayats_range)
        ayat = ayat_with_colon.group(0)[1:]
        send_ayats(chat_id, f'{sura}:{ayat}')
