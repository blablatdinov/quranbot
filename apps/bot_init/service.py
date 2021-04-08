"""Бизнес логика для взаимодействия с телеграмм."""
from time import sleep
from typing import List, Tuple
from django.db.models.query import QuerySet

from loguru import logger
from progressbar import progressbar as pbar
from telebot.apihelper import ApiException

from django.conf import settings
from apps.bot_init.models import Subscriber, SubscriberAction, Message, AdminMessage, Admin
from apps.bot_init.utils import save_message, get_tbot_instance
from apps.bot_init.schemas import SUBSCRIBER_ACTIONS
from apps.bot_init.services.answer_service import Answer, AnswersList
from apps.content.models import MorningContent


SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = settings.BASE_DIR + "/deploy/quranbot-keys.json"
tbot = get_tbot_instance()


def delete_message_in_tg(chat_id: int, message_id: int) -> None:
    """Функция для удаления сообщения в телеграмм."""
    tbot.delete_message(chat_id, message_id)


def get_admins_list() -> List[int]:
    """Функция возвращает список администраторов."""
    return settings.TG_BOT.admins + [admin.subscriber.tg_chat_id for admin in Admin.objects.all()]


def _create_action(subscriber: Subscriber, action: str):
    """Создаем запись в БД о подписке, отписке или реактивации бота пользователем."""
    SubscriberAction.objects.create(subscriber=subscriber, action=action)


def _subscriber_unsubscribed(chat_id: int):
    """Действия, выполняемые при блокировке бота пользователем."""
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    subscriber.is_active = False
    subscriber.save()
    _create_action(subscriber, SUBSCRIBER_ACTIONS[1][0])


def _send_answer(answer: Answer, chat_id: int):  # TODO где будет регистрация tbot
    """Отправляем сообщение пользователю."""
    try:
        if answer.tg_audio_id:
            msg = tbot.send_audio(chat_id, audio=answer.tg_audio_id)
        else:
            msg = tbot.send_message(chat_id, answer.text, reply_markup=answer.keyboard, parse_mode="HTML")
        message_instance = save_message(msg)
        return message_instance
    except ApiException as e:
        if "bot was blocked by the user" in str(e) or "user is deactivated" in str(e) or "chat not found" in str(e):
            _subscriber_unsubscribed(chat_id)
        elif "message text is empty" in str(e):  # TODO законченный контент отлавливается в рассылке сообщений
            send_message_to_admin("Закончился ежедневный контент")
            raise Exception("Закончился ежедневный контент")
        else:
            logger.error(e)
            send_message_to_admin(f"Непредвиденная ошибка\n\n{e}")
            raise e


def send_answer(answer, chat_id) -> Message:
    """Отправляем ответ пользователю.

    Функция может принять как единственный экземпляр класса Answer, так и список экземпляров.
    Поэтому в функции нужна проверка
    """
    if isinstance(answer, list):
        for answer_inst in answer:
            message = _send_answer(answer_inst, chat_id)
    elif isinstance(answer, Answer):
        message = _send_answer(answer, chat_id)
    else:
        raise TypeError(
            "Функция принимает только экземпляры класса Answer или массив экземпляров класса Answer"
            f"Было передано {type(answer)}"
        )
    return message


def send_message_to_admin(message_text: str) -> Message:
    """Отправляем сообщение админу."""
    answer = Answer(message_text)
    admins_tg_chat_ids = get_admins_list()
    for admin_tg_chat_id in admins_tg_chat_ids:
        message_instance = send_answer(answer, admin_tg_chat_id)
    return message_instance


def _not_created_subscriber_service(subscriber: Subscriber) -> Answer:
    """Фунция вызывается если пользователь, который уже существует в базе был корректно обработан."""
    if subscriber.is_active:
        return Answer("Вы уже зарегистрированы", chat_id=subscriber.tg_chat_id)
    _create_action(subscriber, SUBSCRIBER_ACTIONS[2][0])
    subscriber.is_active = True
    subscriber.save(update_fields=["is_active"])
    return Answer(f"Рады видеть вас снова, вы продолжите с дня {subscriber.day}", chat_id=subscriber.tg_chat_id)


def _created_subscriber_service(subscriber: Subscriber) -> List[Answer]:
    """Функция обрабатывает и генерирует ответ для нового подписчика."""
    start_message_text = AdminMessage.objects.get(key="start").text
    day_content = MorningContent.objects.get(day=1).content_for_day()
    _create_action(subscriber, SUBSCRIBER_ACTIONS[0][0])
    answers = [
        Answer(start_message_text, chat_id=subscriber.tg_chat_id),
        Answer(day_content, chat_id=subscriber.tg_chat_id)
    ] + [
        Answer("Зарегестрировался новый пользователь.", chat_id=admin) for admin in get_admins_list()
    ]

    return AnswersList(*answers)


def get_referal_link(subscriber: Subscriber) -> str:
    return f"https://t.me/{settings.TG_BOT.name}?start={subscriber.pk}"


def get_referals_count(subscriber: Subscriber) -> int:
    return Subscriber.objects.filter(referer=subscriber).count()


def get_referal_answer(chat_id: int) -> Answer:
    subscriber = get_subscriber_by_chat_id(chat_id)
    referal_link = get_referal_link(subscriber)
    referals_count = get_referals_count(subscriber)
    text = f"Кол-во пользователей зарегистрировавшихся по вашей ссылке: {referals_count}\n\n{referal_link}"
    return Answer(text=text)


def get_referer(referal_id: int) -> Subscriber:
    logger.debug(f"Getting referal {referal_id=}")
    try:
        return Subscriber.objects.get(pk=referal_id)
    except Subscriber.DoesNotExist as e:
        logger.error(f"Referer with id {referal_id} does not exists")


def get_or_create_subscriber(chat_id: int, referer_subscriber_id: int = None) -> Tuple[Subscriber, bool]:
    if (subscriber_query_set := Subscriber.objects.filter(tg_chat_id=chat_id)).exists():
        logger.debug(f"This chat id was registered")
        subscriber = subscriber_query_set.first()
        created = False
    else:
        referer = None
        if referer_subscriber_id:
            referer = get_referer(referer_subscriber_id)
            send_message_to_referer(referer)
        subscriber = Subscriber.objects.create(
            tg_chat_id=chat_id,
            referer=referer,
        )
        created = True
    return subscriber, created


def registration_subscriber(chat_id: int, referer_subscriber_id: int = None) -> Answer:
    """Логика сохранения подписчика."""
    logger.debug(f"Registration subscriber with {chat_id=} {referer_subscriber_id=}")
    subscriber, created = get_or_create_subscriber(chat_id, referer_subscriber_id=referer_subscriber_id)
    if not created:
        answer = _not_created_subscriber_service(subscriber)
    else:
        answer = _created_subscriber_service(subscriber)
    return answer


def update_webhook(host=f"{settings.TG_BOT.webhook_host}/{settings.TG_BOT.token}"):
    """Обновляем webhook."""
    tbot.remove_webhook()
    sleep(1)
    tbot.set_webhook(host)
    logger.info(tbot.get_webhook_info())


def get_subscriber_by_chat_id(chat_id: int):
    """Получить подписчика по идентификатору."""
    try:
        subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
        return subscriber
    except Subscriber.DoesNotExist:
        logger.info(f"Subscriber {chat_id} does not exist")


def check_user_status_by_typing(chat_id: int):
    """Определить подписан ли пользователь на бота, попробовав отправить сигнал о печати."""
    sub = get_subscriber_by_chat_id(chat_id)
    try:
        tbot.send_chat_action(sub.tg_chat_id, "typing")
        if not sub.is_active:
            sub.is_active = True
            sub.save(update_fields=["is_active"])
        return True
    except Exception as e:
        if ("bot was blocked by the user" in str(e) or "user is deactivated" in str(e)) and sub.is_active:
            _subscriber_unsubscribed(sub.tg_chat_id)


def count_active_users():
    """Подсчитать кол-во активных пользователей."""
    count = 0
    for sub in pbar(Subscriber.objects.all()):
        if check_user_status_by_typing(sub.tg_chat_id):
            count += 1
    return count


def send_message_to_winners(subscribers_queryset: QuerySet):
    text = AdminMessage.objects.get(key="concourse_winner_message").text
    for s in subscribers_queryset:
        Answer(text=text).send(s.tg_chat_id)


def determine_winners():
    referers_pk_list = list(set([
        x[0] for x in 
        Subscriber.objects.filter(is_active=True, referer__isnull=False).values_list("referer")
    ]))
    winners = Subscriber.objects.filter(pk__in=referers_pk_list).exclude(tg_chat_id=224890356).order_by("?")[:3]
    logger.info(f"Winners list={winners}")
    return winners


def commit_concourse():
    winners_quesryset = determine_winners()
    send_message_to_winners(winners_quesryset)
