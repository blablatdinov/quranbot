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
from apps.content.services.podcast_services import get_random_podcast
from apps.content.services.get_unused_ayats import get_unused_ayats
from apps.prayer.exceptions.subscriber_not_set_city import SubscriberNotSetCity
from apps.prayer.models import PrayerAtUser
from apps.prayer.services.get_prayer_times_for_city import PrayerTimeGetter
from apps.prayer.services.prayer_time_for_user import PrayerAtUserGenerator


class AyatDetailView(RetrieveAPIView):
    queryset = Ayat.objects.all()
    serializer_class = AyatSerializer