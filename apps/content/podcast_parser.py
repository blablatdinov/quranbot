import sys

import requests
from bs4 import BeautifulSoup as bs
from loguru import logger

from apps.bot_init.models import Subscriber
from apps.bot_init.service import get_admins_list
from apps.bot_init.utils import save_message
from apps.bot_init.views import tbot
from apps.content.models import AudioFile, Podcast


class PodcastParser:

    def __init__(self):
        ...

    @staticmethod
    def get_subscriber_for_first_sending():
        return Subscriber.objects.get(tg_chat_id=get_admins_list()[0])

    @staticmethod
    def get_last_parsed_podcast_link():
        return AudioFile.objects.last().audio_link if AudioFile.objects.exists() else None

    def send_audio_to_telegram(self, content, title):
        msg = tbot.send_audio(
            self.sub.tg_chat_id, 
            content, 
            timeout=180,
            title=title, 
            performer='Шамиль Аляутдинов'
        )
        return msg

    def create_podcast_instance(self, title, audio_link, msg):
        Podcast.objects.create(
            title=title, 
            audio=AudioFile.objects.create(
                audio_link=audio_link,
                tg_file_id=msg.audio.file_id,
            ),
            flag_for_parser=self.is_first_article
        )

    def create_audio(self, audio_link, title):
        r = requests.get(audio_link)
        if sys.getsizeof(r.content) < 50 * 1024 * 1024:
            msg = self.send_audio_to_telegram(r.content, title)
            save_message(msg)
            self.create_podcast_instance(title, audio_link, msg)
        else:
            AudioFile.objects.create(title=title, audio_link=audio_link)

    def parse_article(self, block):
        link = 'https://umma.ru' + block.find('div', class_='main').find('a')['href']
        soup = bs(requests.get(link).text, 'lxml')
        audio_link = soup.find('audio').find('a')['href']
        title = soup.find('h1').text.strip()
        if audio_link == self.last_audio_in_db_link:
            self.break_flag = True
            return "break"
        else:
            self.create_audio(audio_link, title)

    def parse_page(self, articles_page):
        soup = bs(articles_page.text, 'lxml')
        article_blocks = soup.find_all('article')
        for block in article_blocks:
            if self.parse_article(block) == "break":
                break

    def __call__(self):
        logger.info("Start parsing podcasts...")
        pag_pages = ['https://umma.ru/audlo/shamil-alyautdinov/']
        counter = 1
        self.sub = self.get_subscriber_for_first_sending()
        self.last_audio_in_db_link = self.get_last_parsed_podcast_link()
        self.break_flag = False
        logger.debug(f"{self.last_audio_in_db_link=}")
        iterator = Iterator()

        while True:
            articles_page = requests.get(pag_pages[-1])
            if articles_page.status_code == 404:
                logger.info(f"Last page stop parsing.")
                return
            logger.info(f"Parse {pag_pages[-1]}")

            self.is_first_article = counter == 1

            self.parse_page(articles_page)
            if self.break_flag:
                logger.info(f"{self.break_flag=} stop parsing.")
                break

            # Генерируем ссылки для следующей итерации while
            counter += 1
            pag_pages.append(f'https://umma.ru/audlo/shamil-alyautdinov/page/{counter}')


class Iterator:
    n = 1

    def __iter__(self):
        self.n += 1