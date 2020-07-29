from django.core.management.base import BaseCommand

from bot_init.service import update_webhook


class Command(BaseCommand):
    help = 'command for update webhook'

    def handle(self, *args, **options):
        update_webhook()
