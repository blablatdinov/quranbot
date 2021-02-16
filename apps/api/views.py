from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from loguru import logger

from apps.content.services.podcast_services import get_random_podcast
from apps.api.serializers import AyatSerializer, PodcastSerializer, PrayerAtUserSerializer
from apps.content.models import Ayat, Podcast
from apps.prayer.models import PrayerAtUser
from apps.content.services.ayat_search import get_ayat_by_sura_ayat_numbers


class AyatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ayat.objects.all()
    serializer_class = AyatSerializer

    def get_queryset(self):
        sura_num = self.request.POST.get("sura")
        ayat_num = self.request.POST.get("ayat")
        return get_ayat_by_sura_ayat_numbers(sura_num, ayat_num)


class PodcastViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

    def get_queryset(self):
        return get_random_podcast()


class PrayerAtUserViewSet(viewsets.ReadOnlyModelViewSet):
    """

    Вьюха должна возвращать время намаза по chat_id или по городу
    """
    queryset = PrayerAtUser.objects.all()
    serializer_class = PrayerAtUserSerializer

    # def get_queryset(self):
    #     ...
