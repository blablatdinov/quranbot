from apps.content.models import MorningContent, Ayat


class MorningContentCreator:

    def __init__(self, day: int, ayats_ids: list[int]):
        self.day = day
        self.ayats_ids = ayats_ids

    def __call__(self):
        morning_content = MorningContent.objects.create(
            day=self.day,
        )
        Ayat.objects.filter(pk__in=self.ayats_ids).update(one_day_content=morning_content)
        return MorningContent.objects.filter(pk=morning_content.pk).prefetch_related('ayat_set').first()