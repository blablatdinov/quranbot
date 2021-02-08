from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from loguru import logger

from apps.content.service import find_ayat_by_text, get_random_podcast
from apps.api.serializers import AyatSerializer
from apps.content.models import Ayat
from apps.content.services.ayat_search import get_ayat_by_sura_ayat_numbers


class AyatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ayat.objects.all()
    serializer_class = AyatSerializer

    def get_queryset(self):
        sura_num = self.request.POST.get("sura")
        ayat_num = self.request.POST.get("ayat")
        return get_ayat_by_sura_ayat_numbers(sura_num, ayat_num)