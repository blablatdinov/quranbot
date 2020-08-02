from random import choice

from bot_init.exceptions import AyatDoesNotExists, SuraDoesNotExists, UnknownMessage
from bot_init.schemas import Answer
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

    if not 1 < sura_num < 114:
        raise SuraDoesNotExists

    ayats_in_sura = Ayat.objects.filter(sura=sura_num)  # TODO разнести функцию
    for ayat in ayats_in_sura:
        if '-' in str(ayat):
            low_limit, up_limit = [int(x) for x in str(ayat).split('-')]
            if ayat_num in range(low_limit, up_limit):
                return ayat
        elif ',' in str(ayat):
            name = [int(x) for x in str(ayat).split(',')]
            if ayat_num in name:
                return ayat
        elif int(ayat) == ayat_num:
            return ayat
    raise AyatDoesNotExists


def text_message_service(chat_id: int, message_text: str) -> Answer:
    """Функция обрабатывает все текстовые сообщения"""
    if 'Подкасты' in message_text:
        answer = get_podcast_in_answer_type()
    elif 'Избранное' in message_text:
        ...
    else:
        raise UnknownMessage(message_text)
    return answer
