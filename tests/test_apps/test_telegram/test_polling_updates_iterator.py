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
from typing import Final, Iterable

import httpx
import pytest

from server.apps.telegram.integration.impls.fk_updates_url import FkUpdatesURL
from server.apps.telegram.integration.impls.polling_updates_iterator import PollingUpdatesIterator

FAKE_GET_UPDATES_URL: Final[str] = 'https://api.telegram.org/bot_token/getUpdates'


def _raising_timeout(*args):
    raise httpx.ReadTimeout('')


def test(updates_mock):
    """Проверка списка уведомлений."""
    got = next(PollingUpdatesIterator(
        FkUpdatesURL(FAKE_GET_UPDATES_URL),
        5,
    ))

    assert isinstance(got, list)
    assert len(got) == 1
    assert got[0] == json.dumps(
        updates_mock['result'][0], ensure_ascii=False,
    )


@pytest.mark.usefixtures('_updates_empty_mock')
def test_empty_updates():
    """Проверка списка."""
    got = next(PollingUpdatesIterator(
        FkUpdatesURL(FAKE_GET_UPDATES_URL),
        5,
    ))

    assert isinstance(got, list)
    assert not got


@pytest.mark.usefixtures('_updates_invalid_key')
def test_invalid_key():
    """Проверка невалидного ключа."""
    got = next(PollingUpdatesIterator(
        FkUpdatesURL(FAKE_GET_UPDATES_URL),
        5,
    ))

    assert isinstance(got, list)
    assert not got


@pytest.mark.usefixtures('updates_mock')
def test_iter():
    """Проверка итератора."""
    got = iter(PollingUpdatesIterator(
        FkUpdatesURL(FAKE_GET_UPDATES_URL),
        5,
    ))

    assert isinstance(got, Iterable)


def test_timeout_error(respx_mock):
    """Проверка обработки запроса с ошибкой по таймауту."""
    respx_mock.get(
        FAKE_GET_UPDATES_URL,
    ).mock(side_effect=_raising_timeout)
    got = next(PollingUpdatesIterator(
        FkUpdatesURL(FAKE_GET_UPDATES_URL),
        5,
    ))

    assert isinstance(got, list)
    assert not got
