from django.core.management.base import BaseCommand

from apps.content.podcast_parser import PodcastParser

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        PodcastParser()()
