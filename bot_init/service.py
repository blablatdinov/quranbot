from time import sleep

from telebot import TeleBot
from telebot.apihelper import ApiException

from bot_init.models import Subscriber, AdminMessage, SubscriberAction
from bot_init.utils import save_message
from bot_init.schemas import Answer, SUBSCRIBER_ACTIONS
from config.settings import TG_BOT
from content.models import MorningContent


def _create_subscribed_action(subscriber: Subscriber):  # TODO Может объеденить в одну ф-ю? Индексы сделать как константы
    """Создаем запись в БД о том, что пользователь зарегестрировался"""
    SubscriberAction.objects.create(subscriber=subscriber, action=SUBSCRIBER_ACTIONS[0][0])


def _create_reactivate_action(subscriber: Subscriber):
    """Создаем запись в БД о том, что пользователь реактивировался"""
    SubscriberAction.objects.create(subscriber=subscriber, action=SUBSCRIBER_ACTIONS[2][0])


def _create_unsibscribed_action(subscriber: Subscriber):
    """Создаем запись в БД о том, что пользователь отписался"""
    SubscriberAction.objects.create(subscriber=subscriber, action=SUBSCRIBER_ACTIONS[1][0])


def get_tbot_instance():
    """Получаем экземпляр класса TeleBot для удобной работы с API"""
    return TeleBot(TG_BOT.token)


def _subscriber_unsubscribed(chat_id: int):
    """Действия, выполняемые при блокировке бота пользователем"""
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    subscriber.is_active = False
    subscriber.save()
    _create_unsibscribed_action(subscriber)


def _send_answer(answer: Answer, chat_id: int):  # TODO где будет регистрация tbot? Добавить рассылку аудио файлов
    """Отправляем сообщение пользователю"""
    tbot = get_tbot_instance()
    try:
        if answer.keyboard:
            msg = tbot.send_message(chat_id, answer.text, answer.keyboard)
        else:
            msg = tbot.send_message(chat_id, answer.text)
        message_instance = save_message(msg)
        return message_instance
    except ApiException as e:
        if 'bot was blocked by the user' in str(e):
            _subscriber_unsubscribed(chat_id)
        else:
            ...
            # TODO log, send_to_admin
            # unexpected_error


def send_answer(answer, chat_id):  # FIXME а где у нас try except? Зачем нужны проверки в этой функции?
    """Отправляем ответ пользователю"""
    if isinstance(answer, list):
        for answer_inst in answer:
            _send_answer(answer_inst, chat_id)
    elif isinstance(answer, Answer):
        _send_answer(answer, chat_id)


def send_message_to_admin(message_text: str):  # TODO возможно нужно будет доставать данные из БД
    """Отправляем сообщение админу"""
    answer = Answer(message_text)
    for admin_tg_chat_id in TG_BOT.admins:
        send_answer(answer, admin_tg_chat_id)


def _not_created_subscriber_service(subscriber: Subscriber):
    """Фунция вызывается если пользователь, который уже существует в базе был корректно обработан"""
    if subscriber.is_active:
        return Answer('Вы уже зарегистрированы')
    # TODO добавить блабла вы продолжите с н дня
    _create_reactivate_action(subscriber)
    subscriber.is_active = True
    subscriber.save(update_fields=['is_active'])
    return Answer('Я вернулся')


def _created_subscriber_service(subscriber: Subscriber) -> Answer:
    """Функция обрабатывает и генерирует ответ для нового подписчика"""
    # FIXME здесь стоят загллушки
    # start_message_text = AdminMessage.objects.get(key='start').text
    start_message_text = 'Hello'
    # day_content = MorningContent.objects.get(day=1)
    day_content = 'first day'
    _create_subscribed_action(subscriber)
    send_message_to_admin(
        f'Зарегестрировался новый пользователь.\n\n'
        # TODO можно добавить комманду для статистики
    )
    answers = [
        Answer(start_message_text),
        Answer(day_content)
    ]
    return answers


def registration_subscriber(chat_id: int) -> Answer:
    """Логика сохранения подписчика"""
    # message_text = message.text
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id)
    if not created:
        answer = _not_created_subscriber_service(subscriber)
    else:
        answer = _created_subscriber_service(subscriber, username, first_name, last_name)
    return answer


def update_webhook():
    """Обновляем webhook"""
    tbot = get_tbot_instance()
    tbot.remove_webhook()
    sleep(1)
    web = tbot.set_webhook(f'{TG_BOT.webhook_host}/{TG_BOT.token}')
