import re

import pytest
import requests_mock

from apps.prayer.service import send_prayer_time

pytestmark = [pytest.mark.django_db]


@pytest.mark.freeze_time('2021-03-17')
def test_send_tomorrow_prayer_time(prayers, message_answer, subscriber):
    with requests_mock.Mocker() as m:
        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendMessage.+set_prayer_status_to_read.+"), json=message_answer)  # send prayers
        m.register_uri("POST", re.compile(r"https://api.telegram.org/bot.+/sendMessage\?chat_id=358610865&text=%D0%A0%D0%B0%D1%81%D1%81%D1%8B%D0%BB%D0%BA%D0%B0\+%231\+%D0%B7%D0%B0%D0%B2%D0%B5%D1%80%D1%88%D0%B5%D0%BD%D0%B0&.+"), json=message_answer)  # send message to admin
        send_prayer_time()
