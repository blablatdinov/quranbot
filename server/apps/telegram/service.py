from django.conf import settings

from server.apps.telegram.integration.impls.answer_to_sender import TgAnswerToSender
from server.apps.telegram.integration.impls.empty_answer import TgEmptyAnswer
from server.apps.telegram.integration.impls.message_answer import TgMessageAnswer
from server.apps.telegram.integration.impls.polling_app import PollingApp
from server.apps.telegram.integration.impls.polling_updates_iterator import PollingUpdatesIterator
from server.apps.telegram.integration.impls.sendable_answer import SendableAnswer
from server.apps.telegram.integration.impls.text_answer import TgTextAnswer
from server.apps.telegram.integration.impls.updates_long_polling_url import UpdatesLongPollingURL
from server.apps.telegram.integration.impls.updates_offset_url import UpdatesWithOffsetURL
from server.apps.telegram.integration.impls.updates_url import UpdatesURL
from server.apps.telegram.integration.interfaces.tg_answer import TgAnswer


class EchoAnswer(TgAnswer):

    def build(self, update):
        return TgTextAnswer(
            TgAnswerToSender(
                TgMessageAnswer(
                    TgEmptyAnswer(settings.API_TOKEN),
                ),
            ),
            'hello',
        ).build(update)


class QuranbotAnswer(TgAnswer):

    def build(self, update):
        pass