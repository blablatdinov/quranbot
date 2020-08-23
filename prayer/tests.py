import hashlib
from datetime import datetime, timedelta, time

from django.test import TestCase

from bot_init.models import Subscriber
from prayer.models import Day, City, Prayer, PrayerAtUserGroup, PrayerAtUser
from prayer.schemas import PRAYER_NAMES
from prayer.service import set_city_to_subscriber_by_location, set_city_to_subscriber, get_now_prayer, get_unread_prayers_by_chat_id, generate_prayer_at_user


class GetSetCityTestCase(TestCase):

    def test_set_city_by_location(self):
        Subscriber.objects.create(tg_chat_id=123)
        text = 'Вам будет приходить время намаза для г. Казань'
        answer = set_city_to_subscriber_by_location(('55.81425', '49.078'), 123)
        self.assertEqual(text, answer.text)


class CountUnreadPrayersTestCase(TestCase):

    def test_ok(self):
        subscriber = Subscriber.objects.create(tg_chat_id=123)
        city = City.objects.create(name='Kazan')
        set_city_to_subscriber(city, 123)
        date_time = datetime(2020, 8, 20, 12, 51)
        days = [
            Day.objects.create(date=date_time - timedelta(days=1)),
            Day.objects.create(date=date_time - timedelta(days=2)),
            Day.objects.create(date=date_time)
        ]
        times = [
            time(hour=1, minute=5),
            time(hour=4, minute=0),
            time(hour=12, minute=5),
            time(hour=15, minute=5),
            time(hour=17, minute=5),
            time(hour=20, minute=5),
        ]
        prayer_group = PrayerAtUserGroup.objects.create()

        for day in days:
            for i in range(6):
                prayer = Prayer.objects.create(city=city, day=day, time=times[i], name=PRAYER_NAMES[i][0])
                if prayer.name != 'sunrise':
                    PrayerAtUser.objects.create(subscriber=subscriber, prayer_group=prayer_group, prayer=prayer)

        status = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        queryset = PrayerAtUser.objects.all()
        counter = 0
        for elem in queryset:
            elem.is_read = bool(status[counter])
            elem.save()
            counter += 1
        unread_prayers = get_unread_prayers_by_chat_id(123, datetime(2020, 8, 20, 12, 53))
        self.assertEqual(0, unread_prayers.count())

        status = [
            0, 0, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 0, 0, 0, 0
        ]
        queryset = PrayerAtUser.objects.all()
        counter = 0
        for elem in queryset:
            elem.is_read = bool(status[counter])
            elem.save()
            counter += 1
        unread_prayers = get_unread_prayers_by_chat_id(123, datetime(2020, 8, 20, 12, 53))
        self.assertEqual(2, unread_prayers.count())

        status = [
            1, 1, 0, 1, 1,
            1, 0, 1, 1, 1,
            1, 0, 0, 0, 0
        ]
        # time(hour=1, minute=5),
        # time(hour=12, minute=5),
        # time(hour=15, minute=5),
        # time(hour=17, minute=5),
        # time(hour=20, minute=5),
        # 20.08.2020 16:55
        queryset = PrayerAtUser.objects.all()
        counter = 0
        for elem in queryset:
            elem.is_read = bool(status[counter])
            elem.save()
            counter += 1
        unread_prayers = get_unread_prayers_by_chat_id(123, datetime(2020, 8, 20, 16, 53))
        self.assertEqual(3, unread_prayers.count())


class GetNowPrayerTestCase(TestCase):

    def test_ok(self):
        subscriber = Subscriber.objects.create(tg_chat_id=123)
        city = City.objects.create(name='Kazan')
        set_city_to_subscriber(city, 123)
        date_time = datetime.now()
        day1 = Day.objects.create(date=date_time - timedelta(days=1))
        day2 = Day.objects.create(date=date_time - timedelta(days=2))
        day3 = Day.objects.create(date=date_time)
        times = [
            time(hour=1, minute=5),
            time(hour=4, minute=0),
            time(hour=12, minute=5),
            time(hour=15, minute=5),
            time(hour=17, minute=5),
            time(hour=20, minute=5),
        ]
        prayer_group = PrayerAtUserGroup.objects.create()
        prayers = []
        for i in range(6):
            prayer = Prayer.objects.create(city=city, day=day1, time=times[i], name=PRAYER_NAMES[i][0])
            PrayerAtUser.objects.create(subscriber=subscriber, prayer_group=prayer_group, prayer=prayer)
            prayers.append(prayer)
        for i in range(6):
            prayer = Prayer.objects.create(city=city, day=day2, time=times[i], name=PRAYER_NAMES[i][0])
            PrayerAtUser.objects.create(subscriber=subscriber, prayer_group=prayer_group, prayer=prayer)
            prayers.append(prayer)
        for i in range(6):
            prayer = Prayer.objects.create(city=city, day=day3, time=times[i], name=PRAYER_NAMES[i][0])
            PrayerAtUser.objects.create(subscriber=subscriber, prayer_group=prayer_group, prayer=prayer)
            prayers.append(prayer)

        test_now_value = datetime(day2.date.year, day2.date.month, day2.date.day, hour=2, minute=32)
        now_prayer = get_now_prayer(123, test_now_value)
        self.assertEqual(prayers[6], now_prayer)

        test_now_value = datetime(day1.date.year, day1.date.month, day1.date.day, hour=12, minute=32)
        now_prayer = get_now_prayer(123, test_now_value)
        self.assertEqual(prayers[2], now_prayer)

        test_now_value = datetime(day3.date.year, day3.date.month, day3.date.day, hour=17, minute=4)
        now_prayer = get_now_prayer(123, test_now_value)
        self.assertEqual(prayers[15], now_prayer)

        test_now_value = datetime(day3.date.year, day3.date.month, day3.date.day, hour=9, minute=30)
        now_prayer = get_now_prayer(123, test_now_value)
        self.assertEqual(prayers[13], now_prayer)


class GeneratePrayerAtUserTest(TestCase):

    def test_get(self):
        subscriber = Subscriber.objects.create(tg_chat_id=123)
        city = City.objects.create(name='Kazan')
        set_city_to_subscriber(city, 123)
        date_time = datetime.now()
        day1 = Day.objects.create(date=date_time - timedelta(days=1))
        day2 = Day.objects.create(date=date_time - timedelta(days=2))
        day3 = Day.objects.create(date=date_time)
        times = [
            time(hour=1, minute=5),
            time(hour=4, minute=0),
            time(hour=12, minute=5),
            time(hour=15, minute=5),
            time(hour=17, minute=5),
            time(hour=20, minute=5),
        ]
        for i in range(len(times)):
            prayer = Prayer.objects.create(
                city=city, day=day2, time=times[i], name=PRAYER_NAMES[i][0]
            )
        for i in range(len(times)):
            prayer = Prayer.objects.create(
                city=city, day=day3, time=times[i], name=PRAYER_NAMES[i][0]
            )
        prayer_group = PrayerAtUserGroup.objects.create()
        result = [
            PrayerAtUser.objects.create(subscriber=subscriber, prayer_group=prayer_group, prayer=prayer)
            for prayer in Prayer.objects.filter(day=day3).exclude(name='sunrise')
        ]

        res = generate_prayer_at_user(123, Prayer.objects.filter(day=day3).exclude(name='sunrise'))
        self.assertEqual(result, res)

    def test_gen(self):
        city = City.objects.create(name='Kazan')
        set_city_to_subscriber(city, 123)
        date_time = datetime.now()
        day2 = Day.objects.create(date=date_time - timedelta(days=2))
        day3 = Day.objects.create(date=date_time)
        times = [
            time(hour=1, minute=5),
            time(hour=4, minute=0),
            time(hour=12, minute=5),
            time(hour=15, minute=5),
            time(hour=17, minute=5),
            time(hour=20, minute=5),
        ]
        for i in range(len(times)):
            prayer = Prayer.objects.create(
                city=city, day=day2, time=times[i], name=PRAYER_NAMES[i][0]
            )
        for i in range(len(times)):
            prayer = Prayer.objects.create(
                city=city, day=day3, time=times[i], name=PRAYER_NAMES[i][0]
            )

        res = generate_prayer_at_user(123, Prayer.objects.filter(day=day3).exclude(name='sunrise'))
        h = '9843c44145e7ed8635a8ae1c2ecc7d196c6c0add4096f93502469e3ce3b9d20d'
        self.assertEqual(h, hashlib.sha256(str(res).encode()).hexdigest())
