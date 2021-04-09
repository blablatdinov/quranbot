import sys

import requests
from loguru import logger

from apps.bot_init.models import Subscriber
from apps.bot_init.service import get_admins_list
from apps.bot_init.utils import save_message
from apps.bot_init.views import tbot
from apps.content.models import File, Podcast
from apps.content.parsers import get_html, get_soup


class AchievedLastPageException(Exception):
    pass


class PodcastAlreadyExistException(Exception):
    pass


class PodcastParser:

    def __init__(self):
        ...

    @staticmethod
    def get_subscriber_for_first_sending():
        return Subscriber.objects.get(tg_chat_id=get_admins_list()[0])

    def is_last_page(self, status_code):
        if status_code == 404:
            raise AchievedLastPageException("Достигнута последняя страница")

    def get_articles_links_from_page(self):
        return [
            "https://umma.ru" + x.find("div", class_="main").find("a")["href"] for x in self.article_page_soup.find_all("article")
        ]

    def get_article_info(self, article_link):
        soup = get_soup(get_html(article_link))
        self.link_to_file = soup.find('audio').find('a')['href']
        self.title = soup.find('h1').text.strip()

    def get_articles_page(self):
        response = requests.get(f"https://umma.ru/audlo/shamil-alyautdinov/page/{self.page_num}")
        self.is_last_page(response.status_code)
        self.article_page_soup = get_soup(response.text)

    def send_audio_to_telegram(self, content, title):
        logger.info("Sending...")
        msg = tbot.send_audio(
            self.sub.tg_chat_id, 
            content, 
            timeout=180,
            title=title, 
            performer='Шамиль Аляутдинов'
        )
        return msg

    def download_and_send_audio_file(self):
        logger.info(
            f"Download and send {self.title},\n"
            f"{self.link_to_file=},\n"
            f"{self.article_link=},"
        )
        r = requests.get(self.link_to_file)
        file_size = sys.getsizeof(r.content)
        logger.info(f"file size={file_size / 1024 / 1024} MB")
        if file_size < 50 * 1024 * 1024:
            self.sending_audio_message_instance = self.send_audio_to_telegram(r.content, self.title)
            save_message(self.sending_audio_message_instance)

        is_sended = hasattr(self, "sending_audio_message_instance")
        del r

        self.audio_file = File.objects.create(
            link_to_file=self.link_to_file,
            tg_file_id=self.sending_audio_message_instance.audio.file_id if is_sended else None,
        )
        delattr(self, "sending_audio_message_instance") if is_sended else None # Чтобы на следующей итерации если файл большой, то не присваивать File tg_file_id

    def create_podcast(self):
        Podcast.objects.create(
            title=self.title, 
            article_link = self.article_link,
            audio=self.audio_file,
        )

    def check_article_link_already_parsed(self, article_link):
        return Podcast.objects.filter(article_link=article_link).exists()

    def parse_one_page(self):
        self.get_articles_page()
        for article_link in self.get_articles_links_from_page():
            self.article_link = article_link
            if self.check_article_link_already_parsed(article_link):
                logger.info(f"Find exist podcast {article_link}")
                raise PodcastAlreadyExistException  # TODO протестировать этот момент
            self.get_article_info(article_link)
            self.download_and_send_audio_file()
            self.create_podcast()

    def __call__(self):
        logger.info("Start parsing podcasts...")
        self.page_num = 1
        self.sub = self.get_subscriber_for_first_sending()

        while True:
            try:
                self.parse_one_page()
            except AchievedLastPageException:
                break
            except PodcastAlreadyExistException:
                break
            except Exception as e:
                logger.error(str(e))

            self.page_num += 1

        logger.info("Parsing end")
