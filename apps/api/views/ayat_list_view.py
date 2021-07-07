from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from apps.content.models import Ayat
from apps.content.services.get_unused_ayats import get_unused_ayats
from apps.api.serializers import AyatSerializer


class AyatViewSet(viewsets.ModelViewSet):
    queryset = Ayat.objects.all().select_related('sura')
    serializer_class = AyatSerializer
    permission_classes = [IsAuthenticated]


class NotUsedAyats(generics.ListAPIView):
    """Ayats which not used in morning content"""
    serializer_class = AyatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_unused_ayats()
