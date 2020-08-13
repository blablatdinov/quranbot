import telebot

from bot_init.service import get_tbot_instance
from prayer.models import City


def inline_query_service(city_name: str, query_id: int):
    streets = City.objects.filter(name__icontains=city_name)
    answers = [
        telebot.types.InlineQueryResultArticle(
            id=street.name, title='Город', description=street.name,
            input_message_content=telebot.types.InputTextMessageContent(
                message_text=street.name
            )
        )
        for street in streets
    ]
    get_tbot_instance().answer_inline_query(query_id, answers)
