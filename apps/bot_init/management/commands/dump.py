from django.core.management.base import BaseCommand

from apps.bot_init.services.db_dump_logs_uploader import DumpUploader


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        DumpUploader()()

