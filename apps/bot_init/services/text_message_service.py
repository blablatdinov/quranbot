# TODO Здесь много логики, относящейся к контенту
import re
from typing import List

import requests
from django.conf import settings
from loguru import logger
from telebot.types import InlineKeyboardMarkup

from apps.bot_init.exceptions import AyatDoesNotExists, SuraDoesNotExists, UnknownMessage
from apps.bot_init.markup import InlineKeyboard
from apps.bot_init.models import AdminMessage, Mailing, Subscriber
from apps.bot_init.service import get_admins_list
from apps.bot_init.services.answer_service import Answer, AnswersList
from apps.bot_init.services.concourse import get_referal_link, get_referals_count
from apps.bot_init.services.subscribers import get_subscriber_by_chat_id
from apps.bot_init.utils import get_tbot_instance
from apps.content.models import Ayat, File
from apps.content.service import find_ayat_by_text
from apps.content.services.podcast_services import get_random_podcast_instance
from apps.prayer.models import City
from apps.prayer.service import get_prayer_time_or_no, get_unread_prayers
from apps.prayer.services.geography import set_city_to_subscriber

tbot = get_tbot_instance()


def send_conditions_for_getting_prise(chat_id: int) -> Answer:
    """Отправить условия участия в конкурсе."""
    text = AdminMessage.objects.get(key='conditions').text
    buttons = (
        (('Принять условия', 'accept_with_conditions'),),
    )
    keyboard = InlineKeyboard(buttons)
    return Answer(
        text=text,
        chat_id=chat_id,
        keyboard=keyboard.keyboard,
    )


def get_audio_answer(audio: File) -> Answer:
    """Преобразовать ответ в аудио.

    Если включен режим отладки, и это не основной бот, file_id работать не будут
    """
    if (file_id := audio.tg_file_id) and not settings.DEBUG:
        return Answer(tg_audio_id=file_id)
    return Answer(audio.link_to_file)


def get_podcast_in_answer_type() -> Answer:
    """Получаем подкаст и упаковываем его для отправки пользователю."""
    podcast = get_random_podcast_instance()
    answer = get_audio_answer(podcast.audio)
    return answer


def get_ayat_by_sura_ayat(text: str) -> Ayat:
    """Функция возвращает аят по номеру суры и аята.

    Например: пользователь присылает 2:3, по базе ищется данный аят и возвращает 2:1-5
    """
    sura_num, _ = map(int, text.split(':'))

    if not 1 <= sura_num <= 114:
        raise SuraDoesNotExists

    response = requests.get(f'http://localhost:8001/content/ayats/?q={text}')

    if response.status_code == 400:
        raise AyatDoesNotExists

    ayat_id = response.json()['ayat_id']
    return Ayat.objects.get(pk=ayat_id)


def get_keyboard_for_ayat(ayat: Ayat) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру для сообщения с аятом."""
    if ayat == Ayat.objects.order_by('id').first():
        next_ayat = Ayat.objects.get(pk=ayat.pk + 1)
        buttons = (
            (('Добавить в избранное', f'add_in_favourites({ayat.pk})'),),
            ((str(next_ayat), f'get_ayat({next_ayat.pk})'),),
        )
        return InlineKeyboard(buttons).keyboard
    elif ayat == Ayat.objects.order_by('id').last():
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
                (str(next_ayat), f'get_ayat({next_ayat.pk})'),
            ),
        )
        return InlineKeyboard(buttons).keyboard


def translate_ayat_into_answer(ayat: Ayat) -> List[Answer]:
    """Преобразование аята в Answer."""
    text = (
        f'<a href="https://umma.ru{ayat.sura.link}">({ayat.sura.number}:{ayat.ayat})</a>\n{ayat.arab_text}\n\n'
        f'{ayat.content}\n\n<i>{ayat.trans}</i>\n\n',
    )
    return AnswersList(
        Answer(text=text, keyboard=get_keyboard_for_ayat(ayat)),
        get_audio_answer(ayat.audio)
    )


def delete_messages_in_mailing(mailing_pk: int) -> None:
    """Удалить сообщения в рассылке."""
    messages = Mailing.objects.get(pk=mailing_pk).messages.all()
    for message in messages:
        tbot.delete_message(message.chat_id, message.message_id)


def get_favourite_ayats(chat_id: int) -> Answer:
    """Получить избранные аяты."""
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    ayats = subscriber.favourite_ayats.all()
    if ayats.count():
        text = ''
        for elem in ayats:
            text += f'{str(elem)}\n'
        return Answer(text)
    return Answer('Вы еще не добавили аятов в "Избранное"')


def get_concourse_info(chat_id: int) -> Answer:
    """Получить информацию о конкурсе."""
    subscriber = get_subscriber_by_chat_id(chat_id)
    text = '{}\n\n{}\n\n{}'.format(
        AdminMessage.objects.get(key='concourse').text,
        f'Кол-во пользователей зарегистрировавшихся по вашей ссылке: {get_referals_count(subscriber)}',
        get_referal_link(subscriber),
    )
    return Answer(text=text)


def text_message_service(chat_id: int, message_text: str, message_id: int = None) -> Answer:
    """Функция обрабатывает все текстовые сообщения."""
    if 'Подкасты' in message_text:
        logger.info(f'Subscriber={chat_id} getting random podcast')
        answer = get_podcast_in_answer_type()
    elif 'Избранное' in message_text:
        logger.info(f'Subscriber={chat_id} getting favourite ayats')
        answer = get_favourite_ayats(chat_id)
    elif 'Конкурс' in message_text:
        logger.info(f'Subscriber={chat_id} getting ...')
        answer = get_concourse_info(chat_id)
    elif ':' in message_text:
        logger.info(f'Subscriber={chat_id} search ayat query="{message_text}"')
        try:
            ayat = get_ayat_by_sura_ayat(message_text)
            answer = translate_ayat_into_answer(ayat)
        except AyatDoesNotExists:
            answer = Answer('Аят не найден')
    elif (regexp_result := re.search(r'/del\d+', message_text)) and chat_id in get_admins_list():
        logger.warning(f'Subscriber={chat_id} try delete mailing ayat query="{message_text}"')
        mailing_pk = re.search(r'\d+', regexp_result.group(0)).group(0)
        delete_messages_in_mailing(mailing_pk)
        answer = Answer('Рассылка удалена')
    elif 'Получить дневник' in message_text:
        return send_conditions_for_getting_prise(chat_id)
    elif '/prayer' in message_text:
        return get_unread_prayers(chat_id)
    elif city := City.objects.filter(name=message_text).first():
        logger.warning(f'Subscriber={chat_id} set city')
        answer = set_city_to_subscriber(city, chat_id)
    elif 'Время намаза' in message_text:
        logger.warning(f'Subscriber={chat_id} try get prayer times')
        answer = get_prayer_time_or_no(chat_id)
    elif 'Найти аят' in message_text:
        logger.warning(f'Subscriber={chat_id} set search ayat step')
        sub = Subscriber.objects.get(tg_chat_id=chat_id)
        sub.step = 'search_ayat'
        sub.save()
        return Answer('Введите слово для поиска')
    elif (sub := Subscriber.objects.get(tg_chat_id=chat_id)).step == 'search_ayat':
        logger.warning(f'Subscriber={chat_id} search ayat query="{message_text}"')
        answer = find_ayat_by_text(message_text)
        sub.step = ''
        sub.save()
    else:
        raise UnknownMessage(message_text, message_id)
    return answer
