from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from apps.bot_init.models import Mailing
from apps.api.serializers import MailingSerializer, MailingCreateSerializer
from apps.bot_init.services.mailings import execute_mailing


class Mailings(generics.ListCreateAPIView):
    serializer_class = MailingSerializer

    def get_queryset(self):
        return Mailing.objects.all().prefetch_related('messages')

    def create(self, request):
        serializer = MailingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mailing = execute_mailing(serializer.data['text'])
        return Response(self.serializer_class(mailing).data, status=201)


class MailingDetail(APIView):
    serializer_class = MailingSerializer

    def delete(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.clean()
        return Response(status=204)
