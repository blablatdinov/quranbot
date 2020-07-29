from time import sleep

from telebot import TeleBot

from bot_init.models import Subscriber, AdminMessage, SubscriberAction
from bot_init.utils import save_message
from bot_init.schemas import Answer, SUBSCRIBER_ACTIONS
from config.settings import TG_BOT
from content.models import MorningContent


def get_tbot_instance():
    return TeleBot(TG_BOT.token)


def _send_answer(answer: Answer, chat_id: int):  # TODO где будет регистрация tbot?
    tbot = get_tbot_instance()
    if answer.keyboard:
        msg = tbot.send_message(chat_id, answer.text, answer.keyboard)
    else:
        msg = tbot.send_message(chat_id, answer.text)
    save_message(msg)


def send_answer(answer, chat_id):  # FIXME а где у нас try except?
    if isinstance(answer, list):
        for answer_inst in answer:
            _send_answer(answer_inst, chat_id)
    elif isinstance(answer, Answer):
        _send_answer(answer, chat_id)


def _create_subscribed_action(subscriber: Subscriber):  # TODO Может объеденить в одну ф-ю?
    SubscriberAction.objects.create(subscriber=subscriber, action=SUBSCRIBER_ACTIONS[0][0])


def _create_reactivate_action(subscriber: Subscriber):
    SubscriberAction.objects.create(subscriber=subscriber, action=SUBSCRIBER_ACTIONS[1][0])


def _not_created_subscriber_service(subscriber: Subscriber):
    if subscriber.is_active:
        return Answer('Вы уже зарегистрированы')
    _create_reactivate_action(subscriber)
    subscriber.is_active = True
    subscriber.save(update_fields=['is_active'])
    return Answer('Я вернулся')


def _created_subscriber_service(subscriber: Subscriber, username: str, first_name: str, last_name: str):
    # FIXME здесь стоят загллушки
    # start_message_text = AdminMessage.objects.get(key='start').text
    subscriber.comment = f'first_name: {first_name}\nlast_name: {last_name}\nusername: {username}'
    subscriber.save(update_fields=['comment'])
    start_message_text = 'Hello'
    # day_content = MorningContent.objects.get(day=1)
    day_content = 'first day'
    _create_subscribed_action(subscriber)
    answers = [
        Answer(start_message_text),
        Answer(day_content)
    ]
    return answers


def registration_subscriber(chat_id: int, username: str, first_name: str, last_name: str):
    """Логика сохранения подписчика"""
    # message_text = message.text
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id)
    if not created:
        answer = _not_created_subscriber_service(subscriber)
    else:
        answer = _created_subscriber_service(subscriber, username, first_name, last_name)
    return answer


def update_webhook():
    tbot = get_tbot_instance()
    tbot.remove_webhook()
    sleep(1)
    web = tbot.set_webhook(f'{TG_BOT.webhook_host}/{TG_BOT.token}')
