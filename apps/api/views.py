from rest_framework import viewsets

from apps.content.service import find_ayat_by_text, get_random_podcast
from apps.content.models import Ayat
from apps.api.serializers import AyatSerializer


class AyatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ayat.objects.all()
    serializer_class = AyatSerializer