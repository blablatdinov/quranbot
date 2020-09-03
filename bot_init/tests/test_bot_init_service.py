import os
import re
import random

from dotenv import load_dotenv
from telebot import TeleBot
from django.test import TestCase

from bot_init.service import get_admins_list, get_tbot_instance, _subscriber_unsubscribed, _not_created_subscriber_service, _created_subscriber_service
from bot_init.service import *
from bot_init.service import _create_action
# from bot_init.models import Subscriber, SubscriberAction, AdminMessage
from bot_init.models import *
from bot_init.schemas import Answer
from content.models import Sura


load_dotenv('.env')


class GetAdminListFuncTestCase(TestCase):

    def test_ok(self):
        admins_from_func = get_admins_list()
        admins_from_dotenv = [int(chat_id) for chat_id in os.getenv('ADMINS').split(',')]
        self.assertEqual(admins_from_dotenv, admins_from_func)


class CreateActionTestCase(TestCase):

    def test_subscribed(self):
        subscriber = Subscriber.objects.create(tg_chat_id=2123)
        action_name = 'subscribed'
        _create_action(subscriber, action_name)
        res1 = SubscriberAction.objects.last()
        res2 = SubscriberAction.objects.create(subscriber=subscriber, action=action_name)
        self.assertEqual(res1.action, res2.action)
        self.assertEqual(res1.subscriber, res2.subscriber)

    def test_unsubscribed(self):
        subscriber = Subscriber.objects.create(tg_chat_id=2123)
        action_name = 'unsubscribed'
        _create_action(subscriber, action_name)
        res1 = SubscriberAction.objects.last()
        res2 = SubscriberAction.objects.create(subscriber=subscriber, action=action_name)
        self.assertEqual(res1.action, res2.action)
        self.assertEqual(res1.subscriber, res2.subscriber)

    def test_reactivate(self):
        subscriber = Subscriber.objects.create(tg_chat_id=2123)
        action_name = 'reactivate'
        _create_action(subscriber, action_name)
        res1 = SubscriberAction.objects.last()
        res2 = SubscriberAction.objects.create(subscriber=subscriber, action=action_name)
        self.assertEqual(res1.action, res2.action)
        self.assertEqual(res1.subscriber, res2.subscriber)


class GetInstanceForAPITestCase(TestCase):

    def test_ok(self):
        res1 = get_tbot_instance().get_me().username
        res2 = TeleBot(os.getenv('BOT_TOKEN')).get_me().username
        self.assertEqual(res1, res2)


class SubscriberUnsubscribedTestCase(TestCase):

    def test_ok(self):
        chat_id = 8439934
        Subscriber.objects.create(tg_chat_id=chat_id)
        _subscriber_unsubscribed(chat_id)
        s = Subscriber.objects.last()
        action = SubscriberAction.objects.last().action
        self.assertEqual(s.is_active, False)
        self.assertEqual(action, 'unsubscribed')


class NotNewSubscriberServiceTestCase(TestCase):

    def test_ok(self):
        chat_id = 8439934
        s = Subscriber.objects.create(is_active=False, tg_chat_id=chat_id)
        answer = _not_created_subscriber_service(s)
        self.assertEqual(True, s.is_active)
        self.assertEqual(True, isinstance(answer, Answer))
        self.assertEqual(True, bool(re.search(r'Рады видеть вас снова, вы продолжите с дня \d+', answer.text)))


class NewSubscriberServiceTestCase(TestCase):

    def test_ok(self):
        chat_id = 8439934
        start_message_text = 'Hello'
        AdminMessage.objects.create(key='start', text=start_message_text, title=start_message_text)
        m = MorningContent.objects.create(day=1)
        sura = Sura.objects.create(number=3, link='some_link', child_elements_count=5)
        Ayat.objects.create(
            content='asdf',
            arab_text='asdf',
            trans='asdf',
            sura=sura,
            ayat='3',
            html='<html></html>',
            one_day_content=m
        )
        s = Subscriber.objects.create(tg_chat_id=chat_id)
        answer = _created_subscriber_service(s)
        last_message = Message.objects.last()
        last_message.delete_in_tg()
        self.assertEqual(True, s.is_active)
        self.assertEqual(True, isinstance(answer, list))
        self.assertEqual(2, len(answer))
        self.assertEqual(start_message_text, answer[0].text)


# class TestCase(TestCase):

    # def test_ok(self):
        # ...


# class CountActiveUsersTestCase(TestCase):

    # def test_ok(self):
        # count = 14
        # for i in range(count):
            # chat_id = random.randint(1000, 9999)
            # Subscriber.objects.create(tg_chat_id=chat_id)
        # count_from_func = count_active_users()
        # self.assertEqual(count, count_from_func)
