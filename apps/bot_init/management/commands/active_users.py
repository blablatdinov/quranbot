import os

from django.core.management.base import BaseCommand
from loguru import logger


class Command(BaseCommand):
    help = 'command return count of active users'

    def handle(self, *args, **options):
        logger.info(os.system('./check_users'))

