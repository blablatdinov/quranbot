import json
from datetime import datetime

import pytest
from mixer.backend.django import mixer
from django.conf import settings
import requests_mock


@pytest.fixture()
def city():
    return mixer.blend("prayer.City", name="Казань")


@pytest.fixture()
def subscriber(city):
    return mixer.blend("bot_init.Subscriber", tg_chat_id=358610865, city=city)


@pytest.fixture()
def prayers(city):
    return mixer.cycle(6).blend(
        "prayer.Prayer", 
        day__date=datetime(2021, 3, 18), 
        name=(name for name in ("Иртәнге", "Восход", "Өйлә", "Икенде", "Ахшам", "Ястү",)),
        city=city
    )


@pytest.fixture
def message_answer():
    with open(f"{settings.BASE_DIR}/tests/bot_init/fixture/sended_after_message.json") as f:
        return json.load(f)


@pytest.fixture
def mocker():  # TODO написать общий мокер и прокинуть его в тесты
    mocker = requests_mock.Mocker()
    mocker.adapter_uri()