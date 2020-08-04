import re
from random import choice
from typing import List, Tuple

from bot_init.exceptions import AyatDoesNotExists, SuraDoesNotExists, UnknownMessage
from bot_init.markup import InlineKeyboard
from bot_init.models import Mailing
from bot_init.schemas import Answer
from bot_init.service import get_tbot_instance
from content.models import Podcast, Ayat


def get_random_podcast() -> Podcast:
    """Возвращает рандомный подкаст"""
    podcast = choice(Podcast.objects.all())
    return podcast


def get_podcast_in_answer_type() -> Answer:
    """Получаем подкаст и упаковываем его для отправки пользователю"""
    podcast = get_random_podcast()
    if file_id := podcast.audio.tg_file_id:
        return Answer(tg_audio_id=file_id)
    return Answer(podcast.audio.audio_link)


def get_ayat_by_sura_ayat(text: str) -> Ayat:
    """
    Функция возвращает аят по номеру суры и аята
    Например: пользователь присылает 2:3, по базе ищется данный аят и возвращает 2:1-5
    """
    sura_num, ayat_num = [int(x) for x in text.split(':')]

    if not 1 <= sura_num <= 114:
        raise SuraDoesNotExists

    ayats_in_sura = Ayat.objects.filter(sura=sura_num)  # TODO разнести функцию, не читаемый код
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
    prev_ayat = Ayat.objects.get(pk=ayat.pk - 1)
    next_ayat = Ayat.objects.get(pk=ayat.pk + 1)
    buttons = (
        ((str(prev_ayat), 'wow'), (str(next_ayat), 'wow')),
    )
    return InlineKeyboard(buttons).keyboard


def translate_ayat_into_answer(ayat: Ayat) -> List[Answer]:
    text = f'<b>({ayat.sura}:{ayat.ayat})</b>\n{ayat.arab_text}\n\n{ayat.content}\n\n<i>{ayat.trans}</i>\n\n'
    return [Answer(text=text), Answer(tg_audio_id=ayat.audio.tg_file_id)]


def delete_messages_in_mailing(mailing_pk: int):
    tbot = get_tbot_instance()
    messages = Mailing.objects.get(pk=mailing_pk).messages.all()
    for message in messages:
        tbot.delete_message(message.chat_id, message.message_id)


def text_message_service(chat_id: int, message_text: str) -> Answer:
    """Функция обрабатывает все текстовые сообщения"""
    if 'Подкасты' in message_text:
        answer = get_podcast_in_answer_type()
    elif 'Избранное' in message_text:
        ...
    elif ':' in message_text:
        ayat = get_ayat_by_sura_ayat(message_text)
        answer = translate_ayat_into_answer(ayat)
    elif regexp_result := re.search(r'/del\d+', message_text):
        mailing_pk = re.search(r'\d+', regexp_result.group(0)).group(0)
        delete_messages_in_mailing(mailing_pk)
        answer = Answer('Рассылка удалена')
    else:
        raise UnknownMessage(message_text)
    return answer
