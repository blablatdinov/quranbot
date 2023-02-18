from django.core.management.base import BaseCommand
from django.conf import settings
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

    def handle(self, *args, **options):
        """Entrypoint."""
        PollingApp(
            PollingUpdatesIterator(
                UpdatesLongPollingURL(
                    UpdatesWithOffsetURL(
                        UpdatesURL(settings.API_TOKEN),
                    ),
                    5,
                ),
                5
            ),
            SendableAnswer(
                EchoAnswer(),
            ),
        ).run()
