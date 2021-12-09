import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from apps.bot_init.service import update_webhook


class Command(BaseCommand):
    """Command for update webhook."""

    help = 'command for update webhook'

    def handle(self, *args, **options):
        """Entrypoint."""
        load_dotenv('.env')
        update_webhook(f'{os.getenv("HOST")}/bot_init/{os.getenv("BOT_TOKEN")}')
