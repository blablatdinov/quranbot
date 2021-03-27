"""Бизнес логика для взаимодействия с телеграмм."""
import datetime
import os
from time import sleep
from typing import List, Tuple

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from loguru import logger
from progressbar import progressbar as pbar
from telebot import TeleBot
from telebot.apihelper import ApiException

from django.conf import settings
from apps.bot_init.models import Subscriber, SubscriberAction, Message, AdminMessage, Admin
from apps.bot_init.utils import save_message, get_tbot_instance
from apps.bot_init.schemas import Answer, SUBSCRIBER_ACTIONS
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


def _not_created_subscriber_service(subscriber: Subscriber):
    """Фунция вызывается если пользователь, который уже существует в базе был корректно обработан."""
    if subscriber.is_active:
        return Answer("Вы уже зарегистрированы")
    _create_action(subscriber, SUBSCRIBER_ACTIONS[2][0])
    subscriber.is_active = True
    subscriber.save(update_fields=["is_active"])
    return Answer(f"Рады видеть вас снова, вы продолжите с дня {subscriber.day}")


def _created_subscriber_service(subscriber: Subscriber) -> Answer:
    """Функция обрабатывает и генерирует ответ для нового подписчика."""
    start_message_text = AdminMessage.objects.get(key="start").text
    day_content = MorningContent.objects.get(day=1).content_for_day()
    _create_action(subscriber, SUBSCRIBER_ACTIONS[0][0])
    send_message_to_admin(
        "Зарегестрировался новый пользователь.\n\n"
        # TODO можно добавить комманду для статистики
    )
    answers = [
        Answer(start_message_text),
        Answer(day_content)
    ]
    return answers


def get_referal_link(subscriber: Subscriber) -> str:
    return f"https://t.me/{settings.TG_BOT.name}?start={subscriber.pk}"


def get_referals_scount(subscriber: Subscriber) -> int:
    return Subscriber.objects.filter(referer=subscriber).count()


def get_referal_answer(chat_id: int) -> Answer:
    subscriber = get_subscriber_by_chat_id(chat_id)
    referal_link = get_referal_link(subscriber)
    referals_count = get_referals_scount(subscriber)
    text = f"Кол-во пользователей зарегистрировавшихся по вашей ссылке: {referals_count}\n\n{referal_link}"
    return Answer(text=text)


def send_message_to_referer(referer: Subscriber):
    logger.debug(f"Send message to referal {referer.tg_chat_id=}")
    message = Answer(text="По вашей реферальной ссылке произошла регистрация")
    message = send_answer(message, referer.tg_chat_id)
    # save_message(message)


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


def upload_database_dump():
    """Функция снимает дамп базы данных и загружет его на облако."""
    logger.info("dump start")
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("drive", "v3", credentials=credentials)
    folder_id = "1G_NYTKUHkQixdElU1hOCg4PR2c66zJPB"
    start_time = datetime.datetime.now()

    command = f"pg_dump -U qbot qbot_db -h localhost | gzip -c --best > {settings.BASE_DIR}/deploy/qbot_db.sql.gz"
    os.system(command)
    command = f"pg_dump -U qbot qbot_db -h localhost --exclude-table-data='bot_init_callbackdata' --exclude-table-data='bot_init_message'> {settings.BASE_DIR}/dumps/dev_dump.sql && gzip {settings.BASE_DIR}/dumps/dev_dump.sql -f"
    os.system(command)
    command = f"rm {settings.BASE_DIR}/qbot_db.sql.gz"

    name = "qbot_db.sql.gz"
    file_path = settings.BASE_DIR + "/deploy/qbot_db.sql.gz"
    file_metadata = {
        "name": name,
        "parents": [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    logger.info(f"Dump uploaded successful {datetime.datetime.now() - start_time}")
