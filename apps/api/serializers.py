from rest_framework import serializers

from apps.content.models import Ayat


class AyatSerializer(serializers.ModelSerializer):
    model = Ayat