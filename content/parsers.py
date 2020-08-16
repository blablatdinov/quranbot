""" Модуль содержит парсеры для сайта umma.ru """
import json
import re

import requests
import lxml
from bs4 import BeautifulSoup
from progressbar import progressbar as pbar

from content.models import Ayat, AudioFile


base_url = 'https://umma.ru'


def get_html(url: str) -> str:
    """Функция скачивает html страницу"""
    r = requests.get(url)
    return r.text


def get_soup(html: str) -> BeautifulSoup:
    """Функция преабразует html в soup объект"""
    return BeautifulSoup(html, 'lxml')


class AyatParser:
    """ Класс выполняющий парсинг Корана """
    url = 'https://umma.ru/perevod-korana/'
    current_sura_num = 0
    current_sura_ayat_count: int
    result = []

    def __init__(self):
        ...

    def get_sura(self, soup: BeautifulSoup) -> str:
        """Возвращает суру"""
        return soup.find('h3').text.split(':')[0]

    def get_transcription(self, soup: BeautifulSoup) -> str:
        """Возвращает суру"""
        return soup.find('div', class_='transcription').text.strip()

    def get_arab_text(self, soup: BeautifulSoup) -> str:
        """Возвращает арабский текст"""
        return soup.find('a', class_='quran-speaker').text.strip()

    def get_content(self, soup: BeautifulSoup) -> str:
        """Возвращает содержание перевода"""
        text = ''
        text_block = soup.find('div', class_='text')
        for paragraph in text_block.find_all('p'):
            if (
                '***' in paragraph.text or \
                paragraph.text == 'Ссылки на богословские первоисточники и комментарий:' or \
                'Подробнее см.' in paragraph.text):
                return text
            text += re.sub(r'\[\d+\]', '', paragraph.text)
        return text

    def get_ayat(self, soup: BeautifulSoup) -> str:
        """Возвращает аят"""
        return soup.find('h3').text.split(':')[1]

    def get_sura_links(self):  # -> Generator[str]:
        """ Получаем ссылки на все суры """
        soup = get_soup(get_html(self.url))
        lis = soup.find('ol', class_='items-list').find_all('li')[1:]
        for li in lis:
            yield li.find('a')['href']

    def get_sura_html(self, html: str):  # -> Generator[BeautifulSoup]:
        """ Функция разбивает суру на аяты"""
        soup = get_soup(html)
        blocks = [block for block in soup.find_all('div', class_='quran-block')]
        return blocks

    def get_clean_json(self, text: str) -> str:
        """ Функция убирает лишние символы из строки """
        text = str(text)
        old_new_values = [' ', '', '\n', '', 'label', '"label"', 'value', '"value"', ',]', ']']
        for i in range(0, len(old_new_values) - 1, 2):
            text = text.replace(old_new_values[i], old_new_values[i + 1])
        return text

    def get_ayats_count(self, sura_link: str) -> str:
        """ Функция находит последний аят суры по ссылке """
        soup = get_soup(get_html(base_url + sura_link))
        res = soup.find('v-select')[':options']  # [{"label":"1:1-7","value":"1-1"}]
        clean_json = self.get_clean_json(res)
        res = json.loads(str(clean_json))[-1]  # {"label":"1:1-7","value":"1-1"} - последний dict
        value = res.get('value')  # 1-1
        return value[value.find('-') + 1:]  # 1

    def get_page(self, sura_num: int, sura_ayat_count: int) -> str:
        """ Функция достает все аяты в суре """
        url = f"https://umma.ru/api/v2/quran/{sura_num}"
        payload = f'action=quran&paged={sura_ayat_count}&offset=0'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    def parse_content_from_ayats_in_db(self):
        for ayat in pbar(Ayat.objects.all().order_by('pk')):
        # for ayat in Ayat.objects.filter(pk=209):
            soup = get_soup(ayat.html)
            new_content = self.get_content(soup)
            # try:
            ayat.content = new_content
            ayat.save(update_fields=['content'])
            # except Exception as e:
                # print(ayat)
                # print(new_content)

    def run(self):
        """Запуск парсера"""
        sura_links = self.get_sura_links()
        audio = AudioFile.objects.get(pk=1)  # FIXME сделать нормальный парсинг аудио
        for s in sura_links:
            self.current_sura_num += 1
            self.current_sura_ayat_count = self.get_ayats_count(s)
            page = self.get_page(self.current_sura_num, self.current_sura_ayat_count)
            blocks = self.get_sura_html(page)
            for block in blocks:
                Ayat.objects.create(
                    arab_text=self.get_arab_text(block),
                    trans=self.get_transcription(block),
                    content=''.join([x for x in self.get_content(block)]).replace(
                        'Ссылки на богословские первоисточники и комментарий:',
                        ''
                    ),
                    sura=self.get_sura(block),
                    ayat=self.get_ayat(block),
                    html=str(block),
                    audio=audio,
                    link_to_source=s,
                )
            print(f'Sura {self.current_sura_num} was parsed')


def run_parser():
    parser = AyatParser()
    parser.run()

