from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot

from bot_init.service import registration_subscriber, send_answer, get_tbot_instance
from bot_init.utils import save_message


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


@tbot.message_handler(commands=['start'])  # Обработчик команды старт
def start_handler(message):
    """ Обработчик команды /start """
    save_message(message)
    answer = registration_subscriber(
        chat_id=message.chat.id,
        first_name=message.chat.first_name,
        last_name=message.chat.last_name,
        username=message.chat.username
    )
    send_answer(answer, message.chat.id)
