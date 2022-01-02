from django.conf import settings
from django.db.models import QuerySet
from loguru import logger

from apps.bot_init.models import AdminMessage, Subscriber
from apps.bot_init.services.answer_service import Answer
from apps.bot_init.services.subscribers import get_subscriber_by_chat_id


def send_message_to_winners(subscribers_queryset: QuerySet[Subscriber]) -> None:
    """Отправить сообщение победителям."""
    text = AdminMessage.objects.get(key='concourse_winner_message').text
    for s in subscribers_queryset:
        Answer(text=text).send(s.tg_chat_id)


def determine_winners() -> QuerySet[Subscriber]:
    """Определить победителей."""
    referers_pk_list = list(set([
        x[0] for x in
        Subscriber.objects.filter(is_active=True, referer__isnull=False).values_list('referer')
    ]))
    winners = Subscriber.objects.filter(pk__in=referers_pk_list).exclude(tg_chat_id=224890356).order_by('?')[:3]
    logger.info(f'Winners list={winners}')
    return winners


def get_referal_link(subscriber: Subscriber) -> str:
    """Получить реф. ссылку."""
    return f'Ваша реферальная ссылка: https://t.me/{settings.TG_BOT.name}?start={subscriber.pk}'


def get_referals_count(subscriber: Subscriber) -> int:
    """Получить кол-во рефералов."""
    return Subscriber.objects.filter(referer=subscriber, is_active=True).count()


def get_referal_answer(chat_id: int) -> Answer:
    """Получить ответ на запрос по реф. программе."""
    subscriber = get_subscriber_by_chat_id(chat_id)
    referal_link = get_referal_link(subscriber)
    referals_count = get_referals_count(subscriber)
    text = f'Кол-во пользователей зарегистрировавшихся по вашей ссылке: {referals_count}\n\n{referal_link}'
    return Answer(text=text)


def get_referer(referal_id: int) -> Subscriber:
    """Получить пригласившего."""
    logger.debug(f'Getting referal {referal_id=}')
    try:
        return Subscriber.objects.get(pk=referal_id)
    except Subscriber.DoesNotExist:
        logger.error(f'Referer with id {referal_id} does not exists')


def commit_concourse() -> None:
    """Завершить конкурс."""
    winners_quesryset = determine_winners()
    send_message_to_winners(winners_quesryset)
