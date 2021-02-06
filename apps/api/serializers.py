from rest_framework import serializers

from apps.content.models import Ayat


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
