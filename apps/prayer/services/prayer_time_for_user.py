# FIXME maybe rename module
from datetime import datetime, timedelta

from django.db.models import QuerySet
from loguru import logger

from apps.bot_init.service import get_subscriber_by_chat_id
from apps.prayer.models import Prayer, City, PrayerAtUser, PrayerAtUserGroup
from apps.prayer.exceptions.subscriber_not_set_city import SubscriberNotSetCity

SUNRISE_INDEX = 1


class PrayerAtUserGenerator:

    def __init__(
        self, 
        chat_id: int,
        day: str = "today",
    ) -> None:
        self.chat_id = int(chat_id)
        self._subscriber = get_subscriber_by_chat_id(self.chat_id)
        self.day = day

    def get_prayer_time(
            self,
            city: City, 
            date: datetime,
        ) -> QuerySet:  # TODO а если нужно получать время намаза для определенного дня в API
        """Возвращает время намазов для следующего дня."""
        logger.debug(f"Getting prayers for {city.name}, date: {date}")
        prayers = Prayer.objects.filter(city=city, day__date=date).order_by("pk")
        prayer_group = PrayerAtUserGroup.objects.create()
        self.prayers = [
            PrayerAtUser.objects.create(
                prayer=prayer,
                prayer_group=prayer_group,
                subscriber=self._subscriber
            ) for prayer in prayers
        ]

    def set_attrs(self):
        self.city = self._subscriber.city.name
        self.subscriber_chat_id = self._subscriber.tg_chat_id
        self.sunrise_time = self.prayers[SUNRISE_INDEX].prayer.time
        self.prayers = [
            prayer_time_at_user for prayer_time_at_user in self.prayers 
            if prayer_time_at_user.prayer.name != "sunrise"
        ]

    @staticmethod
    def get_date_by_day(day: str):
        date = {
            "today": datetime.now(),
            "tomorrow": datetime.now() + timedelta(days=1),
        }.get(day)
        return date

    def __call__(self):
        logger.debug(f"Subscriber {self._subscriber} try get prayer_time. Subscriber city: {self._subscriber.city}")

        if self._subscriber.city is None:
            return self._get_city_not_found_answer()

        date = self.get_date_by_day(self.day)
        self.get_prayer_time(self._subscriber.city, date)
        self.set_attrs()
        logger.debug(f"PrayerAtUserGenerator return {self.prayers}")
        return self

    def _get_city_not_found_answer(self):
        """Этот метод возвращает приглашение указать город.

        {
            text: "Вы не указали город, отправьте местоположение или воспользуйтесь поиском",
            button = InlineKeyboardButton("Поиск города", switch_inline_query_current_chat="")
        }

        """
        raise SubscriberNotSetCity
