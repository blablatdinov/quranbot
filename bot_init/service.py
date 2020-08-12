from time import sleep

from telebot import TeleBot
from telebot.apihelper import ApiException
from progressbar import progressbar

from bot_init.models import Subscriber, SubscriberAction, Message, AdminMessage, Admin
from bot_init.utils import save_message
from bot_init.schemas import Answer, SUBSCRIBER_ACTIONS
from config.settings import TG_BOT
from content.models import MorningContent


def get_admins_list():
    return TG_BOT.admins


def _create_action(subscriber: Subscriber, action: str):
    """Создаем запись в БД о подписке, отписке или реактивации бота пользователем"""
    SubscriberAction.objects.create(subscriber=subscriber, action=action)


def get_tbot_instance() -> TeleBot:
    """Получаем экземпляр класса TeleBot для удобной работы с API"""
    return TeleBot(TG_BOT.token)


def _subscriber_unsubscribed(chat_id: int):
    """Действия, выполняемые при блокировке бота пользователем"""
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    subscriber.is_active = False
    subscriber.save()
    _create_action(subscriber, SUBSCRIBER_ACTIONS[1][0])


def _send_answer(answer: Answer, chat_id: int):  # TODO где будет регистрация tbot
    """Отправляем сообщение пользователю"""
    tbot = get_tbot_instance()
    try:
        if answer.tg_audio_id:
            msg = tbot.send_audio(chat_id, audio=answer.tg_audio_id)
        else:
            msg = tbot.send_message(chat_id, answer.text, reply_markup=answer.keyboard, parse_mode='HTML')
        message_instance = save_message(msg)
        return message_instance
    except ApiException as e:
        if 'bot was blocked by the user' in str(e) or 'user is deactivated' in str(e):
            _subscriber_unsubscribed(chat_id)
        elif 'message text is empty' in str(e):  # TODO законченный контент отлавливается в рассылке сообщений
            send_message_to_admin('Закончился ежедневный контент')
            raise Exception('Закончился ежедневный контент')
        else:
            send_message_to_admin(f'Непредвиденная ошибка\n\n{e}')
            # TODO log
            raise e


def send_answer(answer, chat_id) -> Message:
    """
    Отправляем ответ пользователю

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
            'Функция принимает только экземпляры класса Answer или массив экземпляров класса Answer'
            f'Было передано {type(answer)}'
        )
    return message


def send_message_to_admin(message_text: str) -> Message:
    """Отправляем сообщение админу"""
    answer = Answer(message_text)
    admins_tg_chat_ids = TG_BOT.admins + [admin.subscriber.tg_chat_id for admin in Admin.objects.all()]
    for admin_tg_chat_id in admins_tg_chat_ids:
        message_instance = send_answer(answer, admin_tg_chat_id)
    return message_instance


def _not_created_subscriber_service(subscriber: Subscriber):
    """Фунция вызывается если пользователь, который уже существует в базе был корректно обработан"""
    if subscriber.is_active:
        return Answer('Вы уже зарегистрированы')
    _create_action(subscriber, SUBSCRIBER_ACTIONS[2][0])
    subscriber.is_active = True
    subscriber.save(update_fields=['is_active'])
    return Answer(f'Рады видеть вас снова, вы продолжите с дня {subscriber.day}')


def _created_subscriber_service(subscriber: Subscriber) -> Answer:
    """Функция обрабатывает и генерирует ответ для нового подписчика"""
    start_message_text = AdminMessage.objects.get(key='start').text
    day_content = MorningContent.objects.get(day=1).content_for_day()
    _create_action(subscriber, SUBSCRIBER_ACTIONS[0][0])
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
    subscriber, created = Subscriber.objects.get_or_create(tg_chat_id=chat_id)
    if not created:
        answer = _not_created_subscriber_service(subscriber)
    else:
        answer = _created_subscriber_service(subscriber)
    return answer


def update_webhook(host=f'{TG_BOT.webhook_host}/{TG_BOT.token}'):
    """Обновляем webhook"""
    tbot = get_tbot_instance()
    tbot.remove_webhook()
    sleep(1)
    web = tbot.set_webhook(host)


def count_active_users():
    count = 0
    for sub in progressbar(Subscriber.objects.all()):
        try:
            get_tbot_instance().send_chat_action(sub.tg_chat_id, 'typing')
            sub.is_active = True
            sub.save(update_fields=['is_active'])
            count += 1
        except Exception as e:
            if ('bot was blocked by the user' in str(e) or 'user is deactivated' in str(e)):
                if sub.is_active:
                    _subscriber_unsubscribed(sub.tg_chat_id)
            else:
                print(e)
    return f'Count of active users - {count}'
