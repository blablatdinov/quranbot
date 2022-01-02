from typing import List, Optional, Tuple

from loguru import logger

from apps.bot_init.models import Subscriber
from apps.bot_init.service import _created_subscriber_service, _not_created_subscriber_service
from apps.bot_init.services.answer_service import Answer, AnswersList
from apps.bot_init.services.concourse import get_referal_answer


class StartCommandService:
    """Обработчик команды /start."""

    def __init__(self, chat_id: int, message_text: str, additional_info: str = None) -> None:
        self.answers = AnswersList()
        self.chat_id = chat_id
        self.message_text = message_text
        self.additional_info = additional_info
        self.referer = None

    def __call__(self) -> List[Answer]:
        """Entrypoint."""
        if self.additional_info:
            self.referer = self.get_referer(self.additional_info)
            logger.debug(f'Referal of new subscriber={self.additional_info}')
        self.answers += self.registration_subscriber()
        return self.answers

    def get_referer(self, referal_id: int) -> Subscriber:
        """Получить пригласившего."""
        try:
            referer = Subscriber.objects.get(pk=int(referal_id))
        except (Subscriber.DoesNotExist, ValueError) as e:
            logger.error(f'Referer id={referal_id} does not exist. Error={str(e)}')
            referer = None
        return referer

    def generate_message_for_referer(self) -> Answer:
        """Сгенерировать ссылку для пригласившего."""
        logger.debug(f'Send message to referer {self.referer.tg_chat_id=}')
        message = 'По вашей реферальной ссылке произошла регистрация'
        return Answer(text=message, chat_id=self.referer.tg_chat_id)

    def get_or_create_subscriber(self) -> Tuple[Subscriber, bool]:
        """Получить или создать подписчика."""
        if (subscriber_query_set := Subscriber.objects.filter(tg_chat_id=self.chat_id)).exists():
            logger.debug('This chat id was registered')
            subscriber = subscriber_query_set.first()
            created = False
        else:
            if self.referer:
                self.answers.append(self.generate_message_for_referer())
            subscriber = Subscriber.objects.create(
                tg_chat_id=self.chat_id,
                referer=self.referer,
            )
            created = True
        return subscriber, created

    def registration_subscriber(self) -> List[Answer]:
        """Логика сохранения подписчика."""
        logger.info(f'Registration subscriber with {self.chat_id=} {self.referer=}')
        subscriber, created = self.get_or_create_subscriber()
        if not created:
            answers = [_not_created_subscriber_service(subscriber)]
        else:
            answers = _created_subscriber_service(subscriber)
        return answers


class CommandService:
    """Обработчик команд."""

    def __init__(self, chat_id: int, message_text: str) -> None:
        self.chat_id = chat_id
        self.message_text = message_text
        self.additional_info = self.get_additional_info()

    def get_additional_info(self) -> Optional[str]:
        """Получить доп. информацию из сообщения."""
        splitted_string = self.message_text.split()
        if len(splitted_string) > 1:
            logger.debug(f'{splitted_string=}')
            info = splitted_string[1]
            logger.info(f'Command additional info={info}')
            return info

    def __call__(self) -> Answer:
        """Entrypoint."""
        if 'start' in self.message_text:
            answer = StartCommandService(
                chat_id=self.chat_id,
                message_text=self.message_text,
                additional_info=self.additional_info,
            )()
        elif 'referal' in self.message_text:
            answer = get_referal_answer(chat_id=self.chat_id)

        return answer
