from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.api.paginators import Paginator
from apps.api.serializers import MorningContentCreateSerializer, MorningContentSerializer
from apps.content.exceptions.content_too_long import ContentTooLong
from apps.content.models import MorningContent
from apps.content.services.create_morning_content import MorningContentCreator


class MorningContentView(generics.ListCreateAPIView):
    serializer_class = MorningContentSerializer
    pagination_class = Paginator

    def get_queryset(self):
        queryset = MorningContent.objects.all().prefetch_related('ayat_set', 'ayat_set__sura')
        return queryset

    def post(self, request):
        serializer = MorningContentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            morning_content = MorningContentCreator(
                day=serializer.data['day'],
                ayats_ids=serializer.data['ayats_ids'],
            )()
            serializer = MorningContentSerializer(morning_content)
            return Response(serializer.data, status=201)
        except ContentTooLong as e:
            raise ValidationError(detail={'content': [str(e)]})
