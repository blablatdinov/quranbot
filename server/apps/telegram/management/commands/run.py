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
from django.conf import settings
from django.core.management.base import BaseCommand
from loguru import logger

from server.apps.telegram.integration.impls.polling_app import PollingApp
from server.apps.telegram.integration.impls.polling_updates_iterator import PollingUpdatesIterator
from server.apps.telegram.integration.impls.sendable_answer import SendableAnswer
from server.apps.telegram.integration.impls.updates_long_polling_url import UpdatesLongPollingURL
from server.apps.telegram.integration.impls.updates_offset_url import UpdatesWithOffsetURL
from server.apps.telegram.integration.impls.updates_url import UpdatesURL
from server.apps.telegram.service import EchoAnswer

log = logger.bind(task='app')


class Command(BaseCommand):
    """Команда для запуска бота в режиме long polling."""

    help = 'command for start bot long polling mode'

    def handle(self, *args, **options):  # noqa: WPS110. Django API
        """Entrypoint."""
        PollingApp(
            PollingUpdatesIterator(
                UpdatesLongPollingURL(
                    UpdatesWithOffsetURL(
                        UpdatesURL(settings.API_TOKEN),  # type: ignore[misc]
                    ),
                    5,
                ),
                5,
            ),
            SendableAnswer(
                EchoAnswer(),
            ),
        ).run()
