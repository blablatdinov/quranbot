from rest_framework import viewsets
from loguru import logger

from apps.content.services.podcast_services import get_random_podcast
from apps.content.models import Ayat, Podcast
from apps.content.services.ayat_search import get_ayat_by_sura_ayat_numbers
from apps.api.serializers import AyatSerializer, PodcastSerializer, PrayerAtUserGroupSerializer
from apps.prayer.models import PrayerAtUserGroup
from apps.prayer.services.prayer_time_for_user import PrayerAtUserGenerator


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


class PrayerAtUserGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюха должна возвращать время намаза по chat_id или по городу
    """
    queryset = PrayerAtUserGroup.objects.all()
    serializer_class = PrayerAtUserGroupSerializer
    pagination_class = None

    def get_queryset(self):
        chat_id = self.request.query_params.get("chat_id")
        queryset = PrayerAtUserGenerator(chat_id)()
        logger.debug(f"{queryset=}")
        # queryset = PrayerAtUserGroup.objects.filter(prayeratuser__subscriber__tg_chat_id=chat_id)
        return queryset
