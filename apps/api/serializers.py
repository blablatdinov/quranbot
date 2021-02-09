from rest_framework import serializers

from apps.content.models import Ayat, Podcast, AudioFile


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
