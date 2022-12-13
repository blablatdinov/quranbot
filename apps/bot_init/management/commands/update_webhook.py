import os

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.bot_init.service import update_webhook


class Command(BaseCommand):
    """Command for update webhook."""

    help = 'command for update webhook'

    def handle(self, *args, **options):
        """Entrypoint."""
        update_webhook(f'{settings.HOST}/bot_init/{settings.TG_BOT.token}')
