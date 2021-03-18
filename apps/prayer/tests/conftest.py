from datetime import datetime

import pytest
from mixer.backend.django import mixer


@pytest.fixture()
def city():
    return mixer.blend("prayer.City")


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