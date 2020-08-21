

from django.test import TestCase
from bot_init.models import Subscriber
from content.models import Ayat, MorningContent


class MorningContentGen(TestCase):

    def test_ok(self):
        s1 = Subscriber.objects.create(tg_chat_id=12, day=1)
        s2 = Subscriber.objects.create(tg_chat_id=123, day=2)
        m = MorningContent.objects.create(day=1)
        for i in range(5):
            Ayat.objects.create(
                content='asdf', arab_text='asdf', trans='asdf', sura=i + 1,
                ayat='3', html='<html></html>', link_to_source='link', one_day_content=m
            )
        m2 = MorningContent.objects.create(day=2)
        for i in range(5):
            Ayat.objects.create(
                content='asdf', arab_text='asdf', trans='asdf', sura=i + 1,
                ayat='23', html='<html></html>', link_to_source='link', one_day_content=m2
            )
        content1 = MorningContent.objects.get(day=s1.day).content_for_day()
        expected_value = '<b>1:3)</b> asdf\n<b>2:3)</b> asdf\n<b>3:3)</b> asdf\n<b>4:3)</b> asdf\n<b>5:3)</b> asdf\n\nСсылка на источник: <a href="https://umma.rulink">umma.ru</a>'
        self.assertEqual(expected_value, content1)
        content2 = MorningContent.objects.get(day=s2.day).content_for_day()
        expected_value = '<b>1:23)</b> asdf\n<b>2:23)</b> asdf\n<b>3:23)</b> asdf\n<b>4:23)</b> asdf\n<b>5:23)</b> asdf\n\nСсылка на источник: <a href="https://umma.rulink">umma.ru</a>'
        # print(content2)
        self.assertEqual(expected_value, content2)
