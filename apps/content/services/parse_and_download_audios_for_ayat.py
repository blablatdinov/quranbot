from os.path import splitext

from loguru import logger
import requests

from apps.content.models import Ayat, File
from apps.bot_init.views import tbot
from apps.bot_init.service import get_admins_list
from apps.bot_init.utils import save_message


def format_num(number: str) -> str:
    """
    74 -> 074
    2  -> 002
    """
    if "-" in number:
        splitted_num = number.split("-")
        return f"{format_num(splitted_num[0])}-{splitted_num[1]}"
    elif ", " in number:
        splitted_num = [x.strip() for x in number.split(",")]
        logger.debug(f"{splitted_num=}")
        return f"{format_num(splitted_num[0])}-{splitted_num[1]}"
    else:
        a = ["0"] * 3
        b = number[::-1]
        for index, symbol in enumerate(b):
            a[index] = symbol
        return "".join(a)[::-1]


class AyatAudioSaver:

    def __init__(self, ayats_queryset) -> None:
        self.ayats_queryset = ayats_queryset

    @staticmethod
    def get_link_to_audio(ayat: Ayat):
        # https://umma.ru/audio/Ozvucjka-statei/Quran/audio/Husary_64/74/074008-9.mp3
        formatted_sura_num = format_num(str(ayat.sura.number))
        formatted_ayat_num = format_num(ayat.ayat)
        return f"https://umma.ru/audio/Ozvucjka-statei/Quran/audio/Husary_64/{ayat.sura.number}/{formatted_sura_num}{formatted_ayat_num}.mp3"

    @staticmethod
    def send_to_admin(audio, ayat, audio_link):
        logger.info(f"sending audio title={str(ayat)}")
        message = tbot.send_audio(
            get_admins_list()[0], 
            audio, 
            title=str(ayat),
            performer="umma.ru"
        )
        ayat.audio = File.objects.create(
            name=str(ayat),
            link_to_file=audio_link,
            tg_file_id=message.audio.file_id,
        )
        ayat.save()
        save_message(message)

    def __call__(self):
        for ayat in self.ayats_queryset:
            link = self.get_link_to_audio(ayat)
            response = requests.get(link)
            if response.status_code != 200:
                logger.error(f"{ayat=} {response.status_code}")
                continue

            self.send_to_admin(response.content, ayat, link)
