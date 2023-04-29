"""The MIT License (MIT).

Copyright (c) 2018-2023 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
import json
from functools import reduce
from operator import truediv
from typing import Final

import httpx
import pytest
from django.conf import settings

FAKE_GET_UPDATES_URL: Final[str] = 'https://api.telegram.org/bot_token/getUpdates'


@pytest.fixture()
def _updates_empty_mock(respx_mock):
    """Пустой список обновлений."""
    respx_mock.get(
        FAKE_GET_UPDATES_URL,
    ).mock(return_value=httpx.Response(200, json={'ok': True, 'result': []}))


@pytest.fixture()
def updates_mock(respx_mock):
    """Список с обновлением."""
    response = json.loads(
        reduce(
            truediv, [
                settings.BASE_DIR,  # type: ignore[misc]
                'tests',
                'test_apps',
                'test_telegram',
                'fixtures',
                'updates.json',
            ],
        ).read_text(),
    )
    respx_mock.get(
        FAKE_GET_UPDATES_URL,
    ).mock(return_value=httpx.Response(200, json=response))
    return response


@pytest.fixture()
def _updates_invalid_key(respx_mock):
    """Невалидный json."""
    respx_mock.get(
        FAKE_GET_UPDATES_URL,
    ).mock(return_value=httpx.Response(200, json={'list': []}))
