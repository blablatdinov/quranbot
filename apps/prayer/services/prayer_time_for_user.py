# FIXME maybe rename module
from datetime import datetime, timedelta

from django.db.models import QuerySet

from apps.bot_init.service import get_subscriber_by_chat_id
from apps.prayer.models import Prayer, City
from apps.prayer.exceptions.subscriber_not_set_city import SubscriberNotSetCity

class PrayerAtUserGenerator:

    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id
        self._subscriber = get_subscriber_by_chat_id(chat_id)

    @staticmethod
    def get_prayer_time(city: City, date: datetime = datetime.today() + timedelta(days=1)) -> QuerySet:  # TODO а если нужно получать время намаза для определенного дня в API
        """Возвращает время намазов для следующего дня."""
        prayers = Prayer.objects.filter(city=city, day__date=date).order_by("pk")
        return prayers

    def __call__(self):
        if self._subscriber.city is None:
            return self._get_city_not_found_answer()
        today = datetime.now()
        prayers = self.get_prayer_time(self._subscriber.city, today)
        return prayers

    def _get_city_not_found_answer(self):
        """Этот метод возвращает приглашение указать город.

        {
            text: "Вы не указали город, отправьте местоположение или воспользуйтесь поиском",
            button = InlineKeyboardButton("Поиск города", switch_inline_query_current_chat="")
        }

        """
        ...
