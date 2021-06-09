"""Начальная обработка пакетов от телеграмма."""
import telebot
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.bot_init.bot_handlers import tbot


@csrf_exempt
def bot(request):
    """Обработчик пакетов от телеграмма.

    Args:
        request: django.http.HttpRequest

    Raises:
        PermissionDenied: ...

    Returns:
        return: ...
    """
    if request.content_type != 'application/json':
        raise PermissionDenied
    json_data = request.body.decode('utf-8')
    update = telebot.types.Update.de_json(json_data)
    tbot.process_new_updates([update])
    return HttpResponse('')
