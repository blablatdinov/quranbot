from datetime import datetime

from django.db import connection
from django.db import connection
from django.db.models import F

from bot_init.models import Subscriber, Mailing
from bot_init.schemas import Answer
from bot_init.service import send_answer, send_message_to_admin
from bot_init.markup import get_default_keyboard
from content.models import MorningContent


def get_morning_content(day_num: int) -> str:
    """Получаем утренний контент по номеру дня"""
    try:
        content = MorningContent.objects.get(day=day_num).content_for_day()
        return content
    except MorningContent.DoesNotExist:
        text = f'Ежедневный контент для дня {day_num} не найден'
        send_message_to_admin(text)
        # TODO log


def get_subscribers_with_content():
    with connection.cursor() as cursor:
        cursor.execute("""
            select
                s.tg_chat_id,
                STRING_AGG(
                    '<b>' || a.sura::character varying || ': ' || a.ayat || ')</b> ' || a .content || '\n',
                    ''
                    order by a.id
                ),
                STRING_AGG(a.link_to_source, '|' order by a.id)
            from bot_init_subscriber as s
            left join content_morningcontent as mc on s.day=mc.day
            left join content_ayat as a on a.one_day_content_id=mc.id
            where s.is_active='t'
            group by s.tg_chat_id
        """)
        res = cursor.fetchall()
    data = [
            {elem[0]: elem[1] + f'\nСсылка на источник: <a href="https://umma.ru{elem[2].split("|")[0]}">источник</a>'}
            for elem in res
    ]
    return data


def do_morning_content_distribution():
    """Выполняем рассылку утреннего контента"""
    # TODO можно заранее сгенерировать контент, Заранее оповещать админов, что контент кончается
<<<<<<< HEAD
    start = datetime.now()
    with connection.cursor() as cursor:
        cursor.execute("""
            select s.tg_chat_id, s.is_active, s.day, a.sura, a.ayat, a.content
            from bot_init_subscriber as s
            left join content_morningcontent as mc on s.day=mc.day
            left join content_ayat as a on a.one_day_content_id=mc.id
            where s.is_active='t' order by s.tg_chat_id
        """)
        res = cursor.fetchall()
    print(datetime.now() - start)
    start = datetime.now()
    active_subscribers = Subscriber.objects.filter(is_active=True)
=======
>>>>>>> hotfix
    mailing = Mailing.objects.create()
    subscriber_content = get_subscribers_with_content()
    for elem in subscriber_content:
        chat_id, content = list(elem.items())[0]
        answer = Answer(content, keyboard=get_default_keyboard())  # TODO впиши коммент про answers это же не ответ
        continue

        try:
            message_instance = send_answer(answer, chat_id)
            message_instance.mailing = mailing
            message_instance.save(update_fields=['mailing'])
        except:
            pass

<<<<<<< HEAD
        # subscriber.day -= 1
        # subscriber.save(update_fields=['day'])
    print(datetime.now() - start)
    exit()
=======
    for subscriber in Subscriber.objects.filter(is_active=True):
        subscriber.day += 1
        subscriber.save(update_fields=['day'])

>>>>>>> hotfix
    text = f'Рассылка завершена, отправьте /del{mailing.pk} для ее удаления'
    msg = send_message_to_admin(text)
    msg.mailing = mailing
    msg.save(update_fields=['mailing'])
    # FIXME чет дофига длинная функция получается
