"""Бизнес логика для контента."""
from django.db import connection
from django.db.models import F
from loguru import logger

from apps.bot_init.models import Mailing, Subscriber
from apps.bot_init.markup import get_default_keyboard, InlineKeyboard
from apps.bot_init.schemas import Answer
from apps.bot_init.service import send_answer, send_message_to_admin
from apps.content.models import Ayat, MorningContent, Podcast

logger.add("logs/app.log")


def get_random_podcast() -> Podcast:
    """Возвращает рандомный подкаст"""
    podcast = Podcast.objects.order_by("?").first()
    logger.debug(podcast)
    return podcast


def get_morning_content(day_num: int) -> str:
    """Получаем утренний контент по номеру дня."""
    try:
        content = MorningContent.objects.get(day=day_num).content_for_day()
        return content
    except MorningContent.DoesNotExist:
        text = f"Ежедневный контент для дня {day_num} не найден"
        send_message_to_admin(text)
        logger.warning(text)


def get_subscribers_with_content():
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
            where s.tg_chat_id=358610865 or s.tg_chat_id=224890356 and s.day >= 1 and s.is_active='t'
            group by s.tg_chat_id
        """)
        res = cursor.fetchall()
    data = [
            {elem[0]: elem[1] + f"\nСсылка на источник: <a href='https://umma.ru{elem[2].split('|')[0]}'>источник</a>"}
            for elem in res
    ]
    return data


def do_morning_content_distribution():
    """Выполняем рассылку утреннего контента."""
    # TODO можно заранее сгенерировать контент, Заранее оповещать админов, что контент кончается
    mailing = Mailing.objects.create()
    subscriber_content = get_subscribers_with_content()
    for elem in subscriber_content:
        chat_id, content = list(elem.items())[0]
        answer = Answer(content, keyboard=get_default_keyboard())  # TODO впиши коммент про answers это же не ответ

        if message_instance := send_answer(answer, chat_id):
            message_instance.mailing = mailing
            message_instance.save(update_fields=["mailing"])

    Subscriber.objects.filter(is_active=True).update(day=F("day") + 1)

    text = f"Рассылка завершена, отправьте /del{mailing.pk} для ее удаления"
    msg = send_message_to_admin(text)
    msg.mailing = mailing
    msg.save(update_fields=["mailing"])
    # FIXME чет дофига длинная функция получается


def search_ayat(text: str) -> Answer:
    """Функция для поиска аята."""
    queryset = Ayat.objects.filter(content__icontains=text).order_by("pk")
    return queryset


def find_ayat_by_text(query_text: str, offset: int = None):
    """Найти аят по тексту.

    Функция находит аят и определяет страницу

    """
    queryset = search_ayat(query_text)
    logger.debug(queryset)
    result = []
    ayats_count = queryset.count()
    if ayats_count < 1:
        return Answer("Аятов не найдено")
    if offset is None:
        offset = 1
        text = f"По вашему запросу найдено {ayats_count} аятов:"
        result.append(Answer(text))
    buttons = [
        (
            ("<", f"change_query_ayat('{query_text}',{offset - 1})"),
            (f"{offset}/{ayats_count}", "asdf"),
            (">", f"change_query_ayat('{query_text}',{offset + 1})"),
        )
    ]
    keyboard = InlineKeyboard(buttons).keyboard
    ayat = queryset[offset - 1]
    text = ayat.get_content()
    result.append(Answer(text, keyboard))
    return result
