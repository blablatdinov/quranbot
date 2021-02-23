from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

get_prayer_time_doc = {
    "name": "get",
    "decorator": swagger_auto_schema(
        operation_id="Получить время намазов для пользователя или города.",
        manual_parameters=[
            openapi.Parameter(
                "chat_id",
                openapi.IN_QUERY,
                description="Идентификатор чата в телеграм",
                type=openapi.TYPE_STRING,
                # items=openapi.Items(type=openapi.TYPE_INTEGER),
            ),
            openapi.Parameter(
                "city",
                openapi.IN_QUERY,
                description="city",
                type=openapi.TYPE_STRING,  # Вывести список доступных городов
            ),
        ],
    ),
}
