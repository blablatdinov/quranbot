import os

from dotenv import load_dotenv
from telebot import TeleBot

from bot_init.service import get_admins_list, get_tbot_instance
from bot_init.service import _create_action
from bot_init.models import Subscriber, SubscriberAction
from django.test import TestCase


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
        res1 = SubscriberAction.objects.create(subscriber=subscriber, action=action_name)
        res2 = SubscriberAction.objects.last()
        self.assertEqual(res1, res2)

    def test_unsubscribed(self):
        subscriber = Subscriber.objects.create(tg_chat_id=2123)
        action_name = 'unsubscribed'
        res1 = SubscriberAction.objects.create(subscriber=subscriber, action=action_name)
        res2 = SubscriberAction.objects.last()
        self.assertEqual(res1, res2)

    def test_reactivate(self):
        subscriber = Subscriber.objects.create(tg_chat_id=2123)
        action_name = 'reactivate'
        res1 = SubscriberAction.objects.create(subscriber=subscriber, action=action_name)
        res2 = SubscriberAction.objects.last()
        self.assertEqual(res1, res2)


class GetInstanceForAPITestCase(TestCase):

    def test_ok(self):
        res1 = get_tbot_instance().get_me().username
        res2 = TeleBot(os.getenv('BOT_TOKEN')).get_me().username
        self.assertEqual(res1, res2)
