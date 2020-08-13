import os

from dotenv import load_dotenv

from bot_init.service import get_admins_list
from django.test import TestCase


load_dotenv('.env')


class GetAdminListFuncTestCase(TestCase):

    def test_ok(self):
        admins_from_func = get_admins_list()
        admins_from_dotenv = [int(chat_id) for chat_id in os.getenv('ADMINS').split(',')]
        self.assertEqual(admins_from_dotenv, admins_from_func)

