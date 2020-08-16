from django.core.management.base import BaseCommand

from content.parsers import AyatParser


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        p = AyatParser()
        p.parse_content_from_ayats_in_db()
