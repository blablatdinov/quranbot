from typing import List

from apps.content.exceptions import ContentTooLong
from apps.content.models import Ayat, MorningContent


class MorningContentCreator:
    """Класс для создания утреннего контента."""

    def __init__(self, day: int, ayats_ids: List[int]) -> None:
        self.day = day
        self.ayats_ids = ayats_ids
        self._get_target_ayats()

    def _check_ayats_content_length(self) -> None:
        if len(self.morning_content.content_for_day()) > 4096:
            self.morning_content.delete()
            self.target_ayats.update(one_day_content=None)
            raise ContentTooLong

    def _get_target_ayats(self) -> None:
        self.target_ayats = Ayat.objects.filter(pk__in=self.ayats_ids)

    def __call__(self) -> MorningContent:
        """Entrypoint."""
        self.morning_content = MorningContent.objects.create(
            day=self.day,
        )
        self.target_ayats.update(one_day_content=self.morning_content)
        self._check_ayats_content_length()
        return MorningContent.objects.filter(pk=self.morning_content.pk).prefetch_related('ayat_set').first()
