from bot_init.models import Subscriber, Mailing
from bot_init.schemas import Answer
from bot_init.service import send_answer
from content.models import MorningContent


def get_morning_content(day_num: int) -> str:
    try:
        content = MorningContent.objects.get(day=day_num).content_for_day()
        return content
    except MorningContent.DoesNotExist:
        pass
        # TODO log, send to admin, raise Exception


def do_morning_content_distribution():  # TODO можно заранее сгенерировать контент
    active_subscribers = Subscriber.objects.filter(is_active=True)
    mailing = Mailing.objects.create()
    for subscriber in active_subscribers:
        content = get_morning_content(subscriber.day)
        answer = Answer(content)  # TODO впиши коммент про answers это же не ответ

        message_instance = send_answer(answer, subscriber.tg_chat_id)
        message_instance.mailing = mailing
        message_instance.save(update_fields=['mailing'])

        subscriber.day += 1
        subscriber.save(update_fields=['day'])
        # TODO отправлять отчет по рассылке админам
        # FIXME чет дофига длинная функция получается
