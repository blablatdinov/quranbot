"""Бизнес логика для контента."""
from typing import Dict, List, Union

from django.db import connection
from django.db.models import F
from loguru import logger

from apps.bot_init.markup import InlineKeyboard, get_default_keyboard
from apps.bot_init.models import Mailing, Subscriber
from apps.bot_init.service import send_message_to_admin
from apps.bot_init.services.answer_service import Answer
from apps.content.models import Ayat, MorningContent


def get_morning_content(day_num: int) -> str:
    """Получаем утренний контент по номеру дня."""
    try:
        content = MorningContent.objects.get(day=day_num).content_for_day()
        return content
    except MorningContent.DoesNotExist:
        text = f'Ежедневный контент для дня {day_num} не найден'
        send_message_to_admin(text)
        logger.warning(text)


def get_subscribers_with_content() -> Dict:  # FIXME тесты
    """Получаем данные для утренней рассылки одним запросом."""
    with connection.cursor() as cursor:
        cursor.execute("""
            select
                s.tg_chat_id,
                STRING_AGG(
                    '<b>' || sura.number::character varying || ': ' || a.ayat || ')</b> ' || a .content || '\n',
                    ''
                    order by a.id
                ),
                STRING_AGG(sura.link, '|' order by a.id)
            from bot_init_subscriber as s
            left join content_morningcontent as mc on s.day=mc.day
            left join content_ayat as a on a.one_day_content_id=mc.id
            left join content_sura as sura on a.sura_id=sura.id
            where s.is_active = 'true'
            group by s.tg_chat_id
        """)
        res = cursor.fetchall()
    data = []
    for elem in res:
        try:
            data.append({
                elem[0]: (
                    elem[1] + f'\nСсылка на источник: <a href="https://umma.ru{elem[2].split("|")[0]}">источник</a>',
                ),
            })
        except Exception as e:
            logger.error(str(e))
    return data


def _check_morning_content() -> None:
    """Проверка на сколько еще осталось утреннего контента.

    Если менее 10 дней, отправится оповещение админам.
    """
    subscriber_max_day = Subscriber.objects.order_by('day').last().day
    morning_content_max_day = MorningContent.objects.order_by('day').last().day
    if days := (morning_content_max_day - subscriber_max_day) < 4:
        send_message_to_admin(f'Контента осталось на {days}')


def do_morning_content_distribution() -> None:
    """Выполняем рассылку утреннего контента."""
    mailing = Mailing.objects.create()
    subscriber_content = get_subscribers_with_content()
    _check_morning_content()
    for elem in subscriber_content:
        chat_id, content = list(elem.items())[0]
        answer = Answer(content, keyboard=get_default_keyboard())

        if message_instance := answer.send(chat_id):
            message_instance.mailing = mailing
            message_instance.save(update_fields=['mailing'])

    Subscriber.objects.filter(is_active=True).update(day=F('day') + 1)

    text = f'Рассылка #{mailing.pk} завершена.'
    msg = send_message_to_admin(text)
    msg.mailing = mailing
    msg.save(update_fields=['mailing'])


def search_ayat(text: str) -> Answer:
    """Функция для поиска по тексту аята."""
    queryset = Ayat.objects.filter(content__icontains=text).order_by('pk')
    return queryset


def format_count_to_text(number: int) -> str:
    """Отформатировать склонение."""
    div = number % 10
    if number == 11:
        return 'аятов'
    elif div == 1:
        return 'аят'
    elif 1 < div < 5:
        return 'аята'
    elif 4 < number:
        return 'аятов'


def find_ayat_by_text(query_text: str, offset: int = None) -> Union[Answer, List[Answer]]:
    """Найти аят по тексту.

    Функция находит аят и определяет страницу
    """
    queryset = search_ayat(query_text)
    logger.debug(queryset)
    result = []
    ayats_count = queryset.count()
    if ayats_count < 1:
        return Answer('Аятов не найдено')
    if offset is None:
        offset = 1
        text = f'По вашему запросу найдено {ayats_count} {format_count_to_text((ayats_count))}:'
        result.append(Answer(text))
    ayat = queryset[offset - 1]
    buttons = [
        (
            ('Добавить в избранное', f'add_in_favourites({ayat.pk})'),
        ),
        (
            ('<', f'change_query_ayat("{query_text}",{offset - 1})'),
            (f'{offset}/{ayats_count}', 'asdf'),
            ('>', f'change_query_ayat("{query_text}",{offset + 1})'),
        ),
    ]
    keyboard = InlineKeyboard(buttons).keyboard
    text = ayat.get_content()
    result.append(Answer(text, keyboard))
    return result
