"""Начальная обработка пакетов от телеграмма"""
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot
from loguru import logger

from apps.bot_init.service import registration_subscriber, send_answer, get_referal_answer
from apps.bot_init.services.inline_search_service import inline_query_service
from apps.bot_init.services.commands_service import CommandService
from apps.bot_init.services.text_message_service import text_message_service
from apps.bot_init.services.handle_service import handle_query_service
from apps.bot_init.schemas import Answer
from apps.bot_init.utils import save_callback_data, save_message, stop_retry, get_tbot_instance
from apps.prayer.service import set_city_to_subscriber_by_location

tbot = get_tbot_instance()


@csrf_exempt
def bot(request):
    """Обработчик пакетов от телеграмма."""
    if request.content_type == "application/json":
        json_data = request.body.decode("utf-8")
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        return HttpResponse("")
    else:
        raise PermissionDenied


def get_additional_info(text: str) -> str:
    if len(text) > 7:
        return text[7:]


@tbot.message_handler(commands=["start", "referal"])
@stop_retry
def start_handler(message):
    """Обработчик команды /start."""
    logger.info(f"Command handler. Subscriber={message.chat.id} text={message.text}")
    save_message(message)
    answer = CommandService(message.chat.id, message.text)
    send_answer(answer, message.chat.id)


@tbot.message_handler(content_types=["text"])
@stop_retry
def text_handler(message):
    """Обработчик тестовых сообщений в т. ч. некоторых комманд."""
    logger.info(f"Text message handler. Subscriber={message.chat.id}, text={message.text}")
    save_message(message)
    answer = text_message_service(message.chat.id, message.text, message.message_id)
    send_answer(answer, message.chat.id)


@tbot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    """Обравботка нажатий на инлайн кнопку."""
    logger.info(f"Inline button handler. Subscriber={call.from_user.id}, call_data={call.data}, message_id={call.message.message_id}, message_text={call.message.text}, call_id={call.id}")
    save_callback_data(call)
    answer = handle_query_service(
        chat_id=call.from_user.id,
        text=call.data,
        message_id=call.message.message_id,
        message_text=call.message.text,
        call_id=call.id
    )
    if isinstance(answer, Answer) or isinstance(answer, list):
        send_answer(answer, call.from_user.id)


@tbot.message_handler(content_types=["location"])
def handle_location(message):
    """Обравботка геолокации."""
    logger.info(f"Geo location handler.")
    save_message(message)
    answer = set_city_to_subscriber_by_location(
        (message.location.latitude, message.location.longitude),
        message.chat.id
    )
    send_answer(answer, message.chat.id)


@tbot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_query(query):
    """Поиск по названию города."""
    logger.info(f"City search handler. query={query.query}, query_id={query.id}")
    inline_query_service(query.query, query.id)
