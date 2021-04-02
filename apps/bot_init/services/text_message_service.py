# TODO Здесь много логики, относящейся к контенту
import re
from typing import List

from django.conf import settings
from loguru import logger

from apps.bot_init.exceptions import SuraDoesNotExists, UnknownMessage
from apps.bot_init.markup import InlineKeyboard
from apps.bot_init.models import AdminMessage, Mailing, Subscriber
from apps.bot_init.service import get_admins_list, get_referal_link, get_subscriber_by_chat_id, get_referals_count
from apps.bot_init.models import Mailing, Subscriber
from apps.bot_init.services.answer_service import Answer
from apps.bot_init.service import get_admins_list
from apps.bot_init.utils import get_tbot_instance
from apps.bot_init.exceptions import AyatDoesNotExists
from apps.content.models import Podcast, Ayat, AudioFile
from apps.content.service import find_ayat_by_text, get_random_podcast
from apps.prayer.service import get_unread_prayers, set_city_to_subscriber, get_prayer_time_or_no
from apps.prayer.models import City


tbot = get_tbot_instance()


def get_audio_answer(audio: AudioFile) -> Answer:
    if (file_id := audio.tg_file_id) and not settings.DEBUG:
        # Если включен режим отладки, и это не основной бот, file_id работать не будут
        return Answer(tg_audio_id=file_id)
    return Answer(audio.audio_link)


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


def get_concourse_info(chat_id: int) -> Answer:
    text = AdminMessage.objects.get(key="concourse").text
    subscriber = get_subscriber_by_chat_id(chat_id)
    text += f"\n\nКол-во пользователей зарегистрировавшихся по вашей ссылке: {get_referals_count(subscriber)}"
    text += f"\n\n{get_referal_link(subscriber)}"
    return Answer(text=text)


def text_message_service(chat_id: int, message_text: str, message_id: int = None) -> Answer:
    """Функция обрабатывает все текстовые сообщения"""
    if 'Подкасты' in message_text:
        logger.info(f"Subscriber={chat_id} getting random podcast")
        answer = get_podcast_in_answer_type()
    elif 'Избранное' in message_text:
        logger.info(f"Subscriber={chat_id} getting favourite ayats")
        answer = get_favourite_ayats(chat_id)
    elif 'Конкурс' in message_text:
        logger.info(f"Subscriber={chat_id} getting ...")
        answer = get_concourse_info(chat_id)
    elif ':' in message_text:
        logger.info(f"Subscriber={chat_id} search ayat query='{message_text}'")
        try:
            ayat = get_ayat_by_sura_ayat(message_text)
            answer = translate_ayat_into_answer(ayat)
        except AyatDoesNotExists:
            answer = Answer('Аят не найден')
    elif (regexp_result := re.search(r'/del\d+', message_text)) and chat_id in get_admins_list():
        logger.warning(f"Subscriber={chat_id} try delete mailing ayat query='{message_text}'")
        mailing_pk = re.search(r'\d+', regexp_result.group(0)).group(0)
        delete_messages_in_mailing(mailing_pk)
        answer = Answer('Рассылка удалена')
    elif '/prayer' in message_text:
        return get_unread_prayers(chat_id)
    elif city := City.objects.filter(name=message_text).first():
        logger.warning(f"Subscriber={chat_id} set city")
        answer = set_city_to_subscriber(city, chat_id)
    elif 'Время намаза' in message_text:
        logger.warning(f"Subscriber={chat_id} try get prayer times")
        answer = get_prayer_time_or_no(chat_id)
    elif 'Найти аят' in message_text:
        logger.warning(f"Subscriber={chat_id} set search ayat step")
        sub = Subscriber.objects.get(tg_chat_id=chat_id)
        sub.step = 'search_ayat'
        sub.save()
        return Answer("Введите слово для поиска")
    elif (sub := Subscriber.objects.get(tg_chat_id=chat_id)).step == 'search_ayat':
        logger.warning(f"Subscriber={chat_id} search ayat query='{message_text}'")
        answer = find_ayat_by_text(message_text)
        sub.step = ''
        sub.save()
    else:
        raise UnknownMessage(message_text, message_id)
    return answer
