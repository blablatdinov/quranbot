# TODO создать папку для бизнес логики
import re

from bot_init.markup import InlineKeyboard
from bot_init.text_message_service import translate_ayat_into_answer
from bot_init.models import Subscriber
from bot_init.service import get_tbot_instance
from content.models import Ayat
from prayer.models import PrayerAtUser
from prayer.service import get_buttons


def handle_query_service(text: str, chat_id: int = None, call_id: int = None, message_id: int = None, message_text: str = None):
    if 'get_ayat' in text:
        ayat_pk = re.search(r'\d+', text).group(0)
        ayat = Ayat.objects.get(pk=ayat_pk)
        answer = translate_ayat_into_answer(ayat)
        return answer
    elif 'add_in_favourites' in text:
        ayat_pk = re.search(r'\d+', text).group(0)
        ayat = Ayat.objects.get(pk=ayat_pk)
        subscriber = Subscriber.objects.get(tg_chat_id=chat_id)
        subscriber.favourite_ayats.add(ayat)
        subscriber.save()
        get_tbot_instance().answer_callback_query(call_id, show_alert=True, text='Аят добавлен в избранные')
    elif 'change_prayer_status' in text:
        prayer_pk = int(re.search(r'\d+', text).group(0))
        prayer = PrayerAtUser.objects.get(pk=prayer_pk)
        prayer.is_read = not prayer.is_read
        prayer.save()
        keyboard = InlineKeyboard(get_buttons(prayer_pk=prayer_pk)).keyboard
        get_tbot_instance().edit_message_text(
            text=message_text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard
        )


