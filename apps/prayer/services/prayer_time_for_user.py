# FIXME maybe rename module
from datetime import datetime, timedelta, tzinfo

from django.db.models import QuerySet
from django.utils import timezone
from loguru import logger
import pytz

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

    def localize_datetime(self, date_time):
        localized_time = date_time.astimezone(pytz.timezone("Europe/Moscow"))
        logger.debug(f"Localized datetime: {localized_time}")
        return datetime(localized_time.year, localized_time.month, localized_time.day)

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

    def get_date_by_day(self, day: str):
        date = {
            "today": self.time_zone.localize(datetime.now()),
            "tomorrow": self.time_zone.localize(datetime.now()) + timedelta(days=1),
        }.get(day)
        return date

    def __call__(self):
        from apps.prayer.service import get_city_timezone
        logger.debug(f"Subscriber {self._subscriber} try get prayer_time. Subscriber city: {self._subscriber.city}")

        if self._subscriber.city is None:
            return self._get_city_not_found_answer()

        self.time_zone = get_city_timezone(self._subscriber.city.name)
        date = self.get_date_by_day(self.day)
        logger.debug(f"datetime: {date}")
        localized_date = self.localize_datetime(date)
        self.get_prayer_time(self._subscriber.city, localized_date)
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
