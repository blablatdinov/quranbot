from django.core.management.base import BaseCommand, CommandError
from loguru import logger

from apps.bot_init.service import get_tbot_instance, count_active_users


class Command(BaseCommand):
    help = 'command return count of active users'

    def handle(self, *args, **options):
        logger.info(count_active_users())
