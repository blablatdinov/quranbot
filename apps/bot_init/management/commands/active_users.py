import os

from django.core.management.base import BaseCommand
from loguru import logger

from apps.bot_init.service import count_active_users

class Command(BaseCommand):
    help = 'command return count of active users'

    def handle(self, *args, **options):
        count_active_users()

