from apps.prayer.models import PrayerAtUser, PrayerAtUserGroup
from rest_framework import serializers

from apps.content.models import Ayat, Podcast, AudioFile
from apps.prayer.models import PrayerAtUser
from apps.prayer.service import get_text_prayer_times


class AyatSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "additional_content",
            "content",
            "arab_text",
            "trans",
            "sura",
            "ayat",
        )
        model = Ayat


class AudioFileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "audio_link",
            "tg_file_id",
        )
        model = AudioFile


class PodcastSerializer(serializers.ModelSerializer):
    audio = AudioFileSerializer()

    class Meta:
        fields = (
            "title",
            "audio",
        )
        model = Podcast


class PrayerAtUserSerializer(serializers.ModelSerializer):
    subscriber_chat_id = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "subscriber_chat_id",
            "is_read",
            "prayer",
        )
        model = PrayerAtUser

    def get_subscriber_chat_id(self, obj):
        return obj.subscriber.tg_chat_id


class PrayerAtUserGroupSerializer(serializers.ModelSerializer):  # FIXME выкинуть пагинацию
    prayer_data = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "prayer_data",
        )
        model = PrayerAtUserGroup

    def get_prayer_data(self, prayer_group):
        return PrayerAtUserSerializer(prayer_group.prayeratuser_set.all(), many=True).data
