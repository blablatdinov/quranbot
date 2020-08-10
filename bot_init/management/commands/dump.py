from django.core.management.base import BaseCommand, CommandError

from bot_init.service import upload_database_dump


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        upload_database_dump()
