from bot_init.models import Subscriber, Mailing
from bot_init.schemas import Answer
from bot_init.service import send_answer, send_message_to_admin, get_default_keyboard
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


def do_morning_content_distribution():
    """Выполняем рассылку утреннего контента"""
    # TODO можно заранее сгенерировать контент, Заранее оповещать админов, что контент кончается
    active_subscribers = Subscriber.objects.filter(is_active=True)
    mailing = Mailing.objects.create()
    for subscriber in active_subscribers:
        content = get_morning_content(subscriber.day)
        answer = Answer(content, keyboard=get_default_keyboard())  # TODO впиши коммент про answers это же не ответ

        try:
            message_instance = send_answer(answer, subscriber.tg_chat_id)
            message_instance.mailing = mailing
            message_instance.save(update_fields=['mailing'])
        except:
            pass

        subscriber.day += 1
        subscriber.save(update_fields=['day'])
    text = f'Рассылка завершена, отправьте /del{mailing.pk} для ее удаления'
    msg = send_message_to_admin(text)
    msg.mailing = mailing
    msg.save(update_fields=['mailing'])
    # FIXME чет дофига длинная функция получается
