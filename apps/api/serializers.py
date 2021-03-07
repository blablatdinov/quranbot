from rest_framework import serializers

from apps.content.models import AudioFile, Ayat, Podcast, MorningContent
from apps.prayer.models import Prayer, PrayerAtUser


class AyatSerializer(serializers.ModelSerializer):
    sura = serializers.SerializerMethodField()

    def get_sura(self, obj):
        return obj.sura.number

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


class PrayerTimeAtUserInstanceSerializer(serializers.ModelSerializer):
    prayer_name = serializers.SerializerMethodField()
    prayer_time = serializers.SerializerMethodField()

    def get_prayer_name(self, obj):
        return obj.prayer.get_name_display()

    def get_prayer_time(self, obj):
        return obj.prayer.time

    class Meta:
        fields = (
            "id",
            "prayer_name",
            "prayer_time",
            "is_read",
        )
        model = PrayerAtUser


class PrayerAtSubscriberSerializer(serializers.Serializer):
    city = serializers.CharField()
    subscriber_chat_id = serializers.IntegerField()
    sunrise_time = serializers.CharField()
    prayers = PrayerTimeAtUserInstanceSerializer(many=True)


class PrayerTimeSerializer(serializers.ModelSerializer):
    prayer_time = serializers.SerializerMethodField()
    prayer_name = serializers.SerializerMethodField()

    def get_prayer_name(self, obj):
        return obj.get_name_display()

    def get_prayer_time(self, obj):
        return obj.time

    class Meta:
        model = Prayer
        fields = (
            "prayer_name",
            "prayer_time",
        )


class PrayerTimesSerializer(serializers.Serializer):
    city = serializers.CharField()
    sunrise_time = serializers.CharField()
    prayers = PrayerTimeSerializer(many=True)


class SetPrayerStatusSerializer(serializers.Serializer):  # FIXME докинуть валидацию на совпадение id и chat_id
    id = serializers.IntegerField()
    is_read = serializers.BooleanField()
    chat_id = serializers.IntegerField()


class MorningContentSerializer(serializers.ModelSerializer):
    # ayats = AyatSerializer(many=True)

    class Meta:
        model = MorningContent
        fields = (
            "additional_content",
            "day",
            # "ayats",
        )