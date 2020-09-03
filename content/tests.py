from django.test import TestCase

from bot_init.models import Subscriber
from content.models import Ayat, MorningContent, Sura
from content.service import get_subscribers_with_content


class MorningContentGen(TestCase):

    def test_morning_content_method(self):
        s1 = Subscriber.objects.create(tg_chat_id=12, day=1)
        s2 = Subscriber.objects.create(tg_chat_id=123, day=2)
        m = MorningContent.objects.create(day=1)
        for i in range(5):
            sura = Sura.objects.create(number=i + 1, link='link', child_elements_count=5)
            Ayat.objects.create(
                content='asdf', arab_text='asdf', trans='asdf', sura=sura,
                ayat='3', html='<html></html>', one_day_content=m
            )
        m2 = MorningContent.objects.create(day=2)
        for i in range(5):
            sura = Sura.objects.create(number=i + 1, link='link', child_elements_count=5)
            Ayat.objects.create(
                content='asdf', arab_text='asdf', trans='asdf', sura=sura,
                ayat='23', html='<html></html>', one_day_content=m2
            )
        content1 = MorningContent.objects.get(day=s1.day).content_for_day()
        expected_value = '<b>1:3)</b> asdf\n<b>2:3)</b> asdf\n<b>3:3)</b> asdf\n<b>4:3)</b> asdf\n<b>5:3)</b> asdf\n\nСсылка на источник: <a href="https://umma.rulink">umma.ru</a>'
        self.assertEqual(expected_value, content1)
        content2 = MorningContent.objects.get(day=s2.day).content_for_day()
        expected_value = '<b>1:23)</b> asdf\n<b>2:23)</b> asdf\n<b>3:23)</b> asdf\n<b>4:23)</b> asdf\n<b>5:23)</b> asdf\n\nСсылка на источник: <a href="https://umma.rulink">umma.ru</a>'
        self.assertEqual(expected_value, content2)

    def test_query(self):
        s1 = Subscriber.objects.create(tg_chat_id=12, day=1)
        s2 = Subscriber.objects.create(tg_chat_id=123, day=2)
        m = MorningContent.objects.create(day=1)
        for i in range(5):
            sura = Sura.objects.create(number=1, link='link', child_elements_count=5)
            Ayat.objects.create(
                content='asdf', arab_text='asdf', trans='asdf', sura=sura,
                ayat=str(i + 1), html='<html></html>', one_day_content=m
            )
        m2 = MorningContent.objects.create(day=2)
        for i in range(5):
            sura = Sura.objects.create(number=2, link='link', child_elements_count=5)
            Ayat.objects.create(
                content='asdf', arab_text='asdf', trans='asdf', sura=sura,
                ayat=str(i + 2), html='<html></html>', one_day_content=m2
            )
        subscriber_content = get_subscribers_with_content()

