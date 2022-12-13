"""CLI команда для запуска обработчика сообщений.

Classes:
    RecievedEventInterface
    MessagesCreatedEvent
    Command
"""
import asyncio
import json
from typing import Protocol

import nats
from django.conf import settings
from django.core.management.base import BaseCommand
from loguru import logger
from quranbot_schema_registry import validate_schema
from telebot import types

from apps.bot_init.utils import async_save_message


class RecievedEventInterface(Protocol):
    """Интерфейс обрабатываемых событий."""

    event_name: str
    event_version: int

    async def handle_event(self, event_data: dict) -> None:
        """Обработка события.

        :param event_data: dict
        """


class MessagesCreatedEvent(RecievedEventInterface):
    """Событие о создании сообщений."""

    event_name = 'Messages.Created'
    event_version = 1

    async def handle_event(self, event_data: dict) -> None:
        """Обработка события.

        :param event_data: dict
        """
        print(event_data)
        for message in event_data['messages']:
            # from contextlib import suppress
            # with suppress(Exception):
            await async_save_message(
                types.Message.de_json(
                    json.dumps(
                        json.loads(message['message_json'])['message'],
                    ),
                ),
            )


class Command(BaseCommand):
    """Класс для запуска обработчика событий."""

    _handlers = [
        MessagesCreatedEvent(),
    ]
    _queue_name = 'quranbot'

    def handle(self, *args, **kwargs) -> None:  # noqa: WPS110 django API
        """Entrypoint.

        :param args: доп. позиционные аргументы
        :param kwargs: доп. именованные аргументы
        """
        asyncio.run(self._run())

    async def _run(self) -> None:
        """Запуск прослушки jetstream."""
        nats_client = await nats.connect(
            'nats://{0}:{1}'.format(settings.NATS_HOST, settings.NATS_PORT),
            token=settings.NATS_TOKEN,
        )
        logger.info('Start handling events...')
        logger.info('Receive evenst list: {0}'.format([event_handler.event_name for event_handler in self._handlers]))
        js = nats_client.jetstream()
        # await js.add_stream(name="quranbot", subjects=["default"])
        await js.subscribe('quranbot', durable='quranbot_admin', cb=self._message_handler)
        while True:  # noqa: WPS457
            await asyncio.sleep(1)

    async def _message_handler(self, event: bytes) -> None:
        event_dict = json.loads(event.data.decode())
        event_log_data = 'event_id={0} event_name={1} event_version={2}'.format(
            event_dict['event_name'],
            event_dict['event_id'],
            event_dict['event_version'],
        )
        logger.info('Event {0} received'.format(event_log_data))
        try:
            validate_schema(event_dict, event_dict['event_name'], event_dict['event_version'])
        except TypeError as event_validate_error:
            logger.error('Validate {0} failed {1}'.format(event_log_data, str(event_validate_error)))
            return
        for event_handler in self._handlers:
            if self._is_target_event(event_dict, event_handler):
                logger.info('Handling {0} event...'.format(event_log_data))
                await event_handler.handle_event(event_dict['data'])
                logger.info('Event {0} handled successful'.format(event_log_data))
                return
        logger.info('Event {0} skipped'.format(event_log_data))

    def _is_target_event(self, event: dict, event_handler: RecievedEventInterface) -> bool:
        event_name_matched = event_handler.event_name == event['event_name']
        version_matched = event['event_version'] == event_handler.event_version
        return event_name_matched and version_matched
