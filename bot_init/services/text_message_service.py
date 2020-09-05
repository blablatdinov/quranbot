# TODO Здесь много логики, относящейся к контенту
import re
from random import choice
from typing import List, Tuple

from django.conf import settings

from bot_init.exceptions import AyatDoesNotExists, SuraDoesNotExists, UnknownMessage
from bot_init.markup import InlineKeyboard
from bot_init.models import Mailing, Subscriber
from bot_init.schemas import Answer
from bot_init.service import get_tbot_instance, get_admins_list
from bot_init.exceptions import AyatDoesNotExists
from content.models import Podcast, Ayat, AudioFile
from prayer.service import get_unread_prayers, set_city_to_subscriber, get_prayer_time_or_no
from prayer.models import City


def get_audio_answer(audio: AudioFile) -> Answer:
    if (file_id := audio.tg_file_id) and not settings.DEBUG:
        # Если включен режим отладки, и это не основной бот, file_id работать не будут
        return Answer(tg_audio_id=file_id)
    return Answer(audio.audio_link)


def get_random_podcast() -> Podcast:
    """Возвращает рандомный подкаст"""
    podcast = choice(Podcast.objects.all())
    return podcast


def get_podcast_in_answer_type() -> Answer:
    """Получаем подкаст и упаковываем его для отправки пользователю"""
    podcast = get_random_podcast()
    answer = get_audio_answer(podcast.audio)
    return answer


def get_ayat_by_sura_ayat(text: str) -> Ayat:
    """
    Функция возвращает аят по номеру суры и аята
    Например: пользователь присылает 2:3, по базе ищется данный аят и возвращает 2:1-5
    """
    sura_num, ayat_num = [int(x) for x in text.split(':')]

    if not 1 <= sura_num <= 114:
        raise SuraDoesNotExists

    ayats_in_sura = Ayat.objects.filter(sura__number=sura_num)  # TODO разнести функцию, не читаемый код
    for ayat in ayats_in_sura:
        if '-' in str(ayat):
            low_limit, up_limit = [int(x) for x in str(ayat).split(':')[1].split('-')]
            if ayat_num in range(low_limit, up_limit + 1):
                return ayat
        elif ',' in str(ayat):
            name = [int(x) for x in str(ayat).split(':')[1].split(',')]
            if ayat_num in name:
                return ayat
        elif int(ayat.ayat) == ayat_num:
            return ayat
    raise AyatDoesNotExists


def get_keyboard_for_ayat(ayat: Ayat):
    """Возвращает клавиатуру для сообщения с аятом"""
    if ayat == Ayat.objects.first():
        next_ayat = Ayat.objects.get(pk=ayat.pk + 1)
        buttons = (
            (('Добавить в избранное', f'add_in_favourites({ayat.pk})'),),
            ( (str(next_ayat), f'get_ayat({next_ayat.pk})'),),
        )
        return InlineKeyboard(buttons).keyboard
    elif ayat == Ayat.objects.last():
        prev_ayat = Ayat.objects.get(pk=ayat.pk - 1)
        buttons = (
            (('Добавить в избранное', f'add_in_favourites({ayat.pk})'),),
            ((str(prev_ayat), f'get_ayat({prev_ayat.pk})'),),
        )
        return InlineKeyboard(buttons).keyboard
    else:
        next_ayat = Ayat.objects.get(pk=ayat.pk + 1)
        prev_ayat = Ayat.objects.get(pk=ayat.pk - 1)
        buttons = (
            (('Добавить в избранное', f'add_in_favourites({ayat.pk})'),),
            (
                (str(prev_ayat), f'get_ayat({prev_ayat.pk})'), 
                (str(next_ayat), f'get_ayat({next_ayat.pk})')
            ),
        )
        return InlineKeyboard(buttons).keyboard


def translate_ayat_into_answer(ayat: Ayat) -> List[Answer]:
    text = f'<a href="https://umma.ru{ayat.sura.link}">({ayat.sura.number}:{ayat.ayat})</a>\n{ayat.arab_text}\n\n{ayat.content}\n\n<i>{ayat.trans}</i>\n\n'
    return [Answer(text=text, keyboard=get_keyboard_for_ayat(ayat)), get_audio_answer(ayat.audio)]


def delete_messages_in_mailing(mailing_pk: int):
    tbot = get_tbot_instance()
    messages = Mailing.objects.get(pk=mailing_pk).messages.all()
    for message in messages:
        tbot.delete_message(message.chat_id, message.message_id)


def get_favourite_ayats(chat_id: int):
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    ayats = subscriber.favourite_ayats.all()
    if ayats.count():
        text = ''
        for elem in ayats:
            text += f'{str(elem)}\n'
        return Answer(text)
    return Answer('Вы еще не добавили аятов в "Избранное"')


def text_message_service(chat_id: int, message_text: str, message_id: int = None) -> Answer:
    """Функция обрабатывает все текстовые сообщения"""
    if 'Подкасты' in message_text:
        answer = get_podcast_in_answer_type()
    elif 'Избранное' in message_text:
        answer = get_favourite_ayats(chat_id)
    elif ':' in message_text:
        try:
            ayat = get_ayat_by_sura_ayat(message_text)
            answer = translate_ayat_into_answer(ayat)
        except AyatDoesNotExists:
            answer = Answer('Аят не найден')
    elif (regexp_result := re.search(r'/del\d+', message_text)) and chat_id in get_admins_list():
        mailing_pk = re.search(r'\d+', regexp_result.group(0)).group(0)
        delete_messages_in_mailing(mailing_pk)
        answer = Answer('Рассылка удалена')
    elif '/prayer' in message_text:
        return get_unread_prayers(chat_id)
    elif city := City.objects.filter(name=message_text).first():
        answer = set_city_to_subscriber(city, chat_id)
    elif 'Время намаза' in message_text:
        answer = get_prayer_time_or_no(chat_id)
    else:
        raise UnknownMessage(message_text, message_id)
    return answer
