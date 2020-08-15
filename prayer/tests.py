from django.test import TestCase

from bot_init.models import Subscriber
from prayer.service import set_city_to_subscriber_by_location


class GetSetCityTestCase(TestCase):

    def test_set_city_by_location(self):
        Subscriber.objects.create(tg_chat_id=123)
        text = 'Вам будет приходить время намаза для г. Казань'
        answer = set_city_to_subscriber_by_location(('55.81425', '49.078'), 123)
        self.assertEqual(text, answer.text)

