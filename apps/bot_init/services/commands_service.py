from apps.bot_init.utils import save_message
from apps.bot_init.models import Subscriber
from loguru import logger

from apps.bot_init.service import (
    send_answer,
    _not_created_subscriber_service, 
    _created_subscriber_service, 
    get_referal_answer,
)
from apps.bot_init.schemas import Answer


class StartCommandService:
    
    def __init__(self, chat_id: int, message_text: str, additional_info: str = None):
        self.chat_id = chat_id
        self.message_text = message_text
        self.additional_info = additional_info
        self.referer = None

    def __call__(self) -> Answer:
        if self.additional_info:
            self.referer = self.get_referer(self.additional_info)
            logger.debug(f"Referal of new subscriber={self.additional_info}")
        self.registration_subscriber()

    def get_referer(self, referal_id):
        try:
            referer = Subscriber.objects.get(pk=int(referal_id))
        except (Subscriber.DoesNotExist, ValueError) as e:
            logger.error(f"Referer id={referal_id} does not exist. Error={str(e)}")
            referer = None
        return referer

    def send_message_to_referer(self):
        logger.debug(f"Send message to referer {self.referer.tg_chat_id=}")
        message = Answer(text="По вашей реферальной ссылке произошла регистрация")
        message = send_answer(message, self.referer.tg_chat_id)

    def get_or_create_subscriber(self):
        if (subscriber_query_set := Subscriber.objects.filter(tg_chat_id=self.chat_id)).exists():
            logger.debug(f"This chat id was registered")
            subscriber = subscriber_query_set.first()
            created = False
        else:
            if self.referer:
                self.send_message_to_referer()
            subscriber = Subscriber.objects.create(
                tg_chat_id=self.chat_id,
                referer=self.referer,
            )
            created = True
        return subscriber, created

    def registration_subscriber(self):
        """Логика сохранения подписчика."""
        logger.debug(f"Registration subscriber with {self.chat_id=} {self.referer=}")
        subscriber, created = self.get_or_create_subscriber()
        if not created:
            answer = _not_created_subscriber_service(subscriber)
        else:
            answer = _created_subscriber_service(subscriber)
        return answer


class CommandService:

    def __init__(self, chat_id: int, message_text: str):
        self.chat_id = chat_id
        self.message_text = message_text
        self.additional_info = self.get_additional_info()

    def get_additional_info(self):
        if (info := len(self.message_text.split())) > 1:
            info = info[1]
        logger.info(f"Command additional info={info}")
        return info

    def __call__(self) -> Answer:
        if "start" in self.message_text:
            StartCommandService(chat_id=self.chat_id, message_text=self.message_text, additional_info=self.additional_info)
        elif "referal" in self.message_text:
            answer = get_referal_answer(chat_id=self.chat_id)
        return answer

