from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot

from bot_init.handle_service import handle_query_service
from bot_init.inline_search_service import inline_query_service
from bot_init.service import registration_subscriber, send_answer, get_tbot_instance
from bot_init.schemas import Answer
from bot_init.text_message_service import text_message_service
from bot_init.utils import save_message, stop_retry
from prayer.service import set_city_to_subscriber_by_location


tbot = get_tbot_instance()


@csrf_exempt
def bot(request):
    """ Обработчик пакетов от телеграмма """
    if request.content_type == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])
        return HttpResponse('')
    else:
        raise PermissionDenied


@tbot.message_handler(commands=['start'])
@stop_retry
def start_handler(message):
    """ Обработчик команды /start """
    save_message(message)
    answer = registration_subscriber(chat_id=message.chat.id)
    send_answer(answer, message.chat.id)


@tbot.message_handler(content_types=['text'])
@stop_retry
def text_handler(message):
    save_message(message)
    answer = text_message_service(message.chat.id, message.text)
    send_answer(answer, message.chat.id)


@tbot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    call_id = call.id
    chat_id = call.from_user.id
    text = call.data
    message_id = call.message.message_id
    message_text = call.message.text
    print(text)
    answer = handle_query_service(text, chat_id, call_id, message_id, message_text)
    if isinstance(answer, Answer) or isinstance(answer, list):
        send_answer(answer, chat_id)


@tbot.message_handler(content_types=['location'])
def handle_location(message):
    answer = set_city_to_subscriber_by_location(
        (message.location.latitude, message.location.longitude),
        message.chat.id
    )
    send_answer(answer, message.chat.id)


@tbot.inline_handler(func=lambda query: len(query.query) > 0)
def inline_query(query):
    """Поиск по названию города"""
    inline_query_service(query.query, query.id)
