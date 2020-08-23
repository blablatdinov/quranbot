import re
from typing import List

from telebot.types import InlineKeyboardMarkup

from bot_init.markup import InlineKeyboard
from bot_init.schemas import Answer
from bot_init.services.text_message_service import translate_ayat_into_answer
from bot_init.models import Subscriber
from bot_init.service import get_tbot_instance, get_subscriber_by_chat_id
from content.models import Ayat
from prayer.models import PrayerAtUser
from prayer.service import get_buttons, unread_prayer_type_minus_one, get_unread_prayers, get_prayer_time


def _get_ayat(text: str) -> List[Answer]:
    """Получаем аят по pk и возвращам ответ пользователю"""
    ayat_pk = re.search(r'\d+', text).group(0)
    ayat = Ayat.objects.get(pk=ayat_pk)
    answer = translate_ayat_into_answer(ayat)
    return answer


def _unread_prayer_type_minus_one(text: str) -> Answer:
    """
    Парсим идентификатор для схемы PRAYER_NAMES и chat_id подписчика.
    Помечаем намаз прочитанным для подписчика
    """
    regexp_result = re.findall(r'\d+', text)
    prayer_type_id, chat_id = [int(x) for x in regexp_result]
    unread_prayer_type_minus_one(chat_id, prayer_type_id)
    answer = get_unread_prayers(chat_id)
    return answer


def _add_ayat_in_favourites(text: str, chat_id: int) -> str:
    """
    Парсим id аята и добаввляем его в "Избранные" подписчику
    """
    ayat_pk = re.search(r'\d+', text).group(0)
    ayat = Ayat.objects.get(pk=ayat_pk)
    subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
    subscriber.favourite_ayats.add(ayat)
    subscriber.save()
    return 'Аят добавлен в избранные'


def _change_prayer_status(chat_id: int, text: str, to: bool) -> InlineKeyboardMarkup:
    """Меняем статус намаза на прочитанный или не прочитанный"""
    subscriber = get_subscriber_by_chat_id(chat_id)
    prayer_pk = int(re.search(r'\d+', text).group(0))
    prayer = PrayerAtUser.objects.get(pk=prayer_pk)
    prayer.is_read = to
    prayer.save()
    keyboard = InlineKeyboard(get_buttons(subscriber, prayer_at_user_pk=prayer_pk)).keyboard
    return keyboard


def handle_query_service(text: str, chat_id: int = None, call_id: int = None, message_id: int = None, message_text: str = None):
    """Функция для обработки всех нажатий на инлайн кнопки"""
    if 'get_ayat' in text:
        answer = _get_ayat(text)
        return answer
    elif 'add_in_favourites' in text:
        text = _add_ayat_in_favourites(text, chat_id)
        get_tbot_instance().answer_callback_query(call_id, show_alert=True, text=text)
    elif 'set_prayer_status_to_read' in text:
        keyboard = _change_prayer_status(chat_id, text, True)
        get_tbot_instance().edit_message_text(
            text=message_text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard
        )
    elif 'set_prayer_status_to_unread' in text:
        keyboard = _change_prayer_status(chat_id, text, False)
        get_tbot_instance().edit_message_text(
            text=message_text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard
        )
    elif 'unread_prayer_type_minus_one' in text:
        answer = _unread_prayer_type_minus_one(text)
        get_tbot_instance().edit_message_text(
            text=answer.text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=answer.keyboard
        )
