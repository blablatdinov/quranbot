from django.core.management.base import BaseCommand, CommandError

from apps.content.services.parse_and_download_audios_for_ayat import format_num, AyatAudioSaver
from apps.content.models import Ayat

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        AyatAudioSaver(Ayat.objects.filter(audio__isnull=True))()
