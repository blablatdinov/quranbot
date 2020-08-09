from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot

from bot_init.handle_service import handle_query_service
from bot_init.service import registration_subscriber, send_answer, get_tbot_instance
from bot_init.text_message_service import text_message_service
from bot_init.utils import save_message, stop_retry

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
    chat_id = call.from_user.id
    text = call.data
    answer = handle_query_service(text)
    send_answer(answer, chat_id)
