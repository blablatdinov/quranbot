"""Функции, обрататывающие пакеты от телеграмма."""
from loguru import logger

from apps.bot_init.service import send_answer
from apps.bot_init.services.answer_service import Answer
from apps.bot_init.services.commands_service import CommandService
from apps.bot_init.services.handle_service import handle_query_service
from apps.bot_init.services.inline_search_service import inline_query_service
from apps.bot_init.services.text_message_service import text_message_service
from apps.bot_init.utils import (
    get_tbot_instance, 
    save_callback_data,
    save_message, 
    stop_retry,
)
from apps.prayer.service import set_city_to_subscriber_by_location

tbot = get_tbot_instance()


@tbot.message_handler(commands=['start', 'referal'])
@stop_retry
def start_handler(message):
    """Обработчик команды /start.

    Args:
        message: telebot.types.Message
    """
    logger.info(f'Command handler. Subscriber={message.chat.id} text={message.text}')
    save_message(message)
    answers = CommandService(message.chat.id, message.text)()
    answers.send()


@tbot.message_handler(content_types=['text'])
@stop_retry
def text_handler(message):
    """Обработчик тестовых сообщений в т. ч. некоторых комманд.

    Args:
        message: telebot.types.Message
    """
    logger.info(f'Text message handler. Subscriber={message.chat.id}, text={message.text}')
    save_message(message)
    answer = text_message_service(message.chat.id, message.text, message.message_id)
    send_answer(answer, message.chat.id)


@tbot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    """Обработка нажатий на инлайн кнопку.

    Args:
        call: ...

    """
    log_message_template = ''.join(
        'Inline button handler. Subscriber={subscriber_id}, call_data={call_data},',
        'message_id={message_id}, message_text={message_text}, call_id={call_id}',
    )
    log_message = log_message_template.format(
        call.from_user.id,
        call.data,
        call.message_id,
        call.message.text,
        call.id,
    )
    logger.info(log_message)
    save_callback_data(call)
    answer = handle_query_service(
        chat_id=call.from_user.id,
        text=call.data,
        message_id=call.message.message_id,
        message_text=call.message.text,
        call_id=call.id,
    )
    if isinstance(answer, (Answer, list)):
        send_answer(answer, call.from_user.id)


@tbot.message_handler(content_types=['location'])
def handle_location(message):
    """Обработка геолокации.

    Args:
        message: telebot.types.Message
    """
    logger.info('Geo location handler.')
    save_message(message)
    answer = set_city_to_subscriber_by_location(
        tuple(message.location.latitude, message.location.longitude),
        message.chat.id,
    )
    send_answer(answer, message.chat.id)


@tbot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_query(query):
    """Поиск по названию города.

    Args:
        query: telebot.types.Message
    """
    logger.info(f'City search handler. query={query.query}, query_id={query.id}')
    inline_query_service(query.query, query.id)
