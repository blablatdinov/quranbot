from django.utils.decorators import method_decorator
from loguru import logger
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.exceptions.chat_id_or_city_not_gived import (
    ChatIdOrCityNotGived, SubscriberNotDefinedCityAPIException)
from apps.api.schemas.swagger_schemas import get_prayer_time_doc
from apps.api.serializers import (AyatSerializer, PodcastSerializer,
                                  PrayerAtSubscriberSerializer,
                                  PrayerTimeAtUserInstanceSerializer,
                                  PrayerTimesSerializer,
                                  SetPrayerStatusSerializer)
from apps.content.models import Podcast, Ayat
from apps.content.services.ayat_search import get_ayat_by_sura_ayat_numbers
from apps.content.services.podcast_services import get_random_podcast
from apps.prayer.exceptions.subscriber_not_set_city import SubscriberNotSetCity
from apps.prayer.models import PrayerAtUser
from apps.prayer.services.get_prayer_times_for_city import PrayerTimeGetter
from apps.prayer.services.prayer_time_for_user import PrayerAtUserGenerator


class AyatAPIView(ListAPIView):
    serializer_class = AyatSerializer

    def get_queryset(self):
        sura_num = self.request.query_params.get('sura')
        ayat_num = self.request.query_params.get('ayat')
        res = get_ayat_by_sura_ayat_numbers(sura_num, ayat_num)
        logger.debug(f'{res=}')
        return res


class PodcastViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

    def get_queryset(self):
        return get_random_podcast()


@method_decorator(**get_prayer_time_doc)
class PrayerTimeView(APIView):  # FIXME слишком толстые методы
    """
    Вьюха должна возвращать время намаза по chat_id или по городу
    """
    # TODO кейс если закончилось время намаза

    def get(self, request):
        chat_id = request.query_params.get('chat_id')
        city = request.query_params.get('city')
        if not (chat_id or city):
            raise ChatIdOrCityNotGived

        if chat_id:
            try:
                prayers_data = PrayerAtUserGenerator(chat_id=int(chat_id))()
                serialized_data = PrayerAtSubscriberSerializer(
                    prayers_data,
                ).data
                return Response(serialized_data)
            except SubscriberNotSetCity:
                raise SubscriberNotDefinedCityAPIException
        elif city:
            prayers_data = PrayerTimeGetter(city)()
            serialized_data = PrayerTimesSerializer(
                prayers_data,
            ).data
            return Response(serialized_data)

    def put(self, request):
        serialized_data = SetPrayerStatusSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data = serialized_data.data
            prayer_at_user = PrayerAtUser.objects.get(id=serialized_data.get('id'))
            prayer_at_user.is_read = serialized_data.get('is_read')
            prayer_at_user.save()
            serialized_data = PrayerTimeAtUserInstanceSerializer(prayer_at_user).data
            return Response(serialized_data, status=201)
        else:
            logger.debug(f'{serialized_data.errors=}')


class AyatDetailView(RetrieveAPIView):
    queryset = Ayat.objects.all()
    serializer_class = AyatSerializer


class NotUsedAyats(ListAPIView):
    """Ayats which not used in morning content"""
    serializer_class = AyatSerializer

    def get_queryset(self):
        Ayat.objects.filter()
