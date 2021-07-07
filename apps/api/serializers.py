from rest_framework import serializers

from apps.content.models import File, Ayat, Podcast
from apps.prayer.models import Prayer, PrayerAtUser


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'link_to_file',
            'tg_file_id',
        )
        model = File


class PodcastSerializer(serializers.ModelSerializer):
    audio = FileSerializer()

    class Meta:
        fields = (
            'title',
            'audio',
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
            'id',
            'prayer_name',
            'prayer_time',
            'is_read',
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
            'prayer_name',
            'prayer_time',
        )


class PrayerTimesSerializer(serializers.Serializer):
    city = serializers.CharField()
    sunrise_time = serializers.CharField()
    prayers = PrayerTimeSerializer(many=True)


class SetPrayerStatusSerializer(serializers.Serializer):  # FIXME докинуть валидацию на совпадение id и chat_id
    id = serializers.IntegerField()
    is_read = serializers.BooleanField()
    chat_id = serializers.IntegerField()
