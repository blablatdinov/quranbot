"""Модуль содержит парсеры для сайта (https://umma.ru)."""
# FIXME сделать нормальный парсинг аудио
import hashlib
import re

from bs4 import BeautifulSoup
from loguru import logger
import requests
from progressbar import progressbar as pbar

from apps.content.models import Ayat, Sura

logger.add("logs/app.log")
base_url = "https://umma.ru"


def get_html(url: str) -> str:
    """Функция скачивает html страницу."""
    r = requests.get(url)
    return r.text


def get_soup(html: str) -> BeautifulSoup:
    """Функция преабразует html в soup объект."""
    return BeautifulSoup(html, "lxml")


class AyatParser:
    """Класс выполняющий парсинг Корана."""

    url = "https://umma.ru/perevod-korana/"
    current_sura_num = 0
    current_sura_ayat_count: int
    result = []

    def __init__(self):
        ...

    @staticmethod
    def get_sura(soup: BeautifulSoup) -> str:
        """Возвращает суру."""
        return soup.find("h3").text.split(":")[0]

    @staticmethod
    def get_transcription(soup: BeautifulSoup) -> str:
        """Возвращает транслитерацию аята."""
        return soup.find("div", class_="transcription").text.strip()

    @staticmethod
    def get_arab_text(soup: BeautifulSoup) -> str:
        """Возвращает арабский текст."""
        return soup.find("a", class_="quran-speaker").text.strip()

    @staticmethod
    def get_content(soup: BeautifulSoup) -> str:
        """Возвращает содержание перевода."""
        text = ""
        text_block = soup.find("div", class_="text")
        for paragraph in text_block.find_all("p"):
            if (
                    "***" in paragraph.text or
                    paragraph.text == "Ссылки на богословские первоисточники и комментарий:" or
                    "Подробнее см." in paragraph.text
            ):
                return text
            text += re.sub(r"\[\d+\]", "", paragraph.text)  # TODO вынести в очищение контента
        return text

    def parse_content_from_db(self):
        for ayat in pbar(Ayat.objects.all()):
            ayat.content = "".join([x for x in self.get_content(get_soup(ayat.html))]).replace(
                # FIXME починить очистку текста
                "Ссылки на богословские первоисточники и комментарий:",
                ""
            )
            ayat.save()

    @staticmethod
    def get_ayat(soup: BeautifulSoup) -> str:
        """Возвращает номер аята."""
        return soup.find("h3").text.split(":")[1]

    def get_sura_links(self):
        """Получаем ссылки на все суры."""
        soup = get_soup(get_html(self.url))
        lis = soup.find("ol", class_="items-list").find_all("li")[1:]
        for li in lis:
            yield li.find("a")["href"]

    @staticmethod
    def get_sura_html(html: str):
        """Функция разбивает суру на аяты."""
        soup = get_soup(html)
        blocks = [block for block in soup.find_all("div", class_="quran-block")]
        return blocks

    @staticmethod
    def get_page(sura_num: int, sura_ayat_count: int) -> str:
        """Функция достает все аяты в суре."""
        url = f"https://umma.ru/api/v2/quran/{sura_num}"
        payload = f"action=quran&paged={sura_ayat_count}&offset=0"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    def run(self):
        """Запуск парсера."""
        for sura in Sura.objects.all():
            page = self.get_page(sura.number, sura.child_elements_count)
            if hashlib.sha256(str(page).encode()).hexdigest() == sura.pars_hash:
                logger.info(f"Sura #{sura.number} not changed")
                continue
            sura.pars_hash = hashlib.sha256(str(page).encode()).hexdigest()
            sura.save(update_fields=["pars_hash"])

            blocks = self.get_sura_html(page)
            for block in blocks:
                ayat, created = Ayat.objects.get_or_create(
                    arab_text=self.get_arab_text(block),
                    sura=sura,
                    ayat=self.get_ayat(block),
                )
                # if not created:
                ayat.trans = self.get_transcription(block),
                ayat.content = "".join([x for x in self.get_content(block)]).replace(
                    # FIXME починить очистку текста
                    "Ссылки на богословские первоисточники и комментарий:",
                    ""
                )
                ayat.html = str(block)
                ayat.save()

            logger.info(f"Sura {sura.number} was parsed")


def run_parser():
    """Функция для удобного запуска парсера."""
    parser = AyatParser()
    parser.run()
