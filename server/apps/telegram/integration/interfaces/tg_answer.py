from typing import Protocol

import httpx

from server.apps.telegram.integration.interfaces.update import Update


class TgAnswer(Protocol):

    def build(self, update: Update) -> list[httpx.Request]:
        pass
