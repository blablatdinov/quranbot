from loguru import logger

from apps.content.models import Ayat

from apps.bot_init.services.text_message_service import get_ayat_by_sura_ayat
from apps.bot_init.exceptions import AyatDoesNotExists


def get_ayat_by_sura_ayat_numbers(sura_number: int, ayat_number: int):
    logger.info(f"{sura_number}:{ayat_number}")
    if sura_number and ayat_number:
        logger.info(f"Search {sura_number}:{ayat_number}")
        queryset = Ayat.objects.filter(sura__number=sura_number, ayat=ayat_number)
        return queryset
    queryset = Ayat.objects.all()
    return queryset


class AyatSearcher:

    def __init__(self, sura_number: int, ayat_number: int):
        self.sura_number = sura_number
        self.ayat_number = ayat_number

    def _hyphen_cases(self, ayat):
        low_limit, up_limit = [int(x) for x in str(ayat).split(':')[1].split('-')]
        if self.ayat_number in range(low_limit, up_limit + 1):
            return ayat

    def _comma_separated_cases(self, ayat):
        name = [int(x) for x in str(ayat).split(':')[1].split(',')]
        print(f"{name=}")
        if self.ayat_number in name:
            return ayat

    def _check_ayat(self, ayat):
        print(f"{ayat=}")
        if '-' in str(ayat):  # Для кейсов типа 2:1-5
            print("case 1")
            return self._hyphen_cases(ayat)
        elif ',' in str(ayat):  # Для кейсов типа 3:5,6
            print("case 2")
            return self._comma_separated_cases(ayat)
        elif int(ayat.ayat) == self.ayat_number:  # Для кейсов, когда название можно перевести в чиcло
            print("case 3")
            return ayat

    def get_ayat_by_sura_ayat(self) -> Ayat:
        """
        Функция возвращает аят по номеру суры и аята
        Например: пользователь присылает 2:3, по базе ищется данный аят и возвращает 2:1-5
        """

        if not 1 <= self.sura_number <= 114:
            raise SuraDoesNotExists

        ayats_in_sura = Ayat.objects.filter(sura__number=self.sura_number)  # TODO разнести функцию, не читаемый код
        for ayat in ayats_in_sura:
            a = self._check_ayat(ayat)
            print(f"self._check_ayat(ayat) = {a}")
            return self._check_ayat(ayat)
        raise AyatDoesNotExists

    def __call__(self):
        if self.sura_number and self.ayat_number:
            return self.get_ayat_by_sura_ayat()
