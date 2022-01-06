from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import MailingCreateSerializer, MailingSerializer
from apps.bot_init.models import Mailing
from apps.bot_init.services.mailings import execute_mailing


class Mailings(generics.ListCreateAPIView):
    serializer_class = MailingSerializer

    def get_queryset(self):
        return Mailing.objects.all().prefetch_related('messages')

    def create(self, request):
        """Создание рассылки.

        TODO: Перенести на golang
        """
        serializer = MailingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mailing = execute_mailing(serializer.data['text'])
        return Response(self.serializer_class(mailing).data, status=201)


class MailingDetail(APIView):
    serializer_class = MailingSerializer

    def delete(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.clean_messages()
        return Response(status=204)
