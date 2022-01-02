import ujson
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from loguru import logger

from apps.bot_init.models import Admin, AdminMessage, CallbackData, Mailing, Message, Subscriber, SubscriberAction
from apps.content.models import File


class SubscriberActionInline(admin.StackedInline):
    """Действие подписчика."""

    model = SubscriberAction
    extra = 0


class DisplayMailingFilter(admin.SimpleListFilter):
    """Фильтр позволяет отключить отображение рассылок в административной панели."""

    title = "Отображать сообщения"
    parameter_name = "hz"

    def lookups(self, request, model_admin):
        """В списке res указываем правило фильтрации."""
        res = [
            ("without_mailings", "Без рассылок"),
            ("unknown_messages", "Необработанные сообщения"),
        ]
        return res

    def queryset(self, request, queryset):
        """В методе определяется правила фильтрации."""
        if self.value() == "without_mailings":
            return queryset.filter(mailing__isnull=True)
        elif self.value() == "unknown_messages":
            return queryset.filter(is_unknown=True)
        return queryset


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Класс для конфигурации сообщения в админке."""

    list_display = (
        "get_mailing_or_source", "date", "message_id", "get_message_text"
    )
    exclude = ('json',)
    search_fields = ("text", "from_user_id", "chat_id")
    readonly_fields = (
        'date', 'from_user_id', 'message_id', 'chat_id', 'text', 'is_unknown', 'get_formatted_json',
    )
    list_filter = (DisplayMailingFilter,)

    def _count_spaces_in_start_line(self, line) -> int:
        for i, x in enumerate(line):
            if x != ' ':
                return i

        return 0

    def get_formatted_json(self, message: Message):
        """Форматирование json'a для админки."""
        text_lines = ujson.dumps(eval(message.json), indent=2, ensure_ascii=False).split('\n')
        res = []
        for line in text_lines:
            indent = self._count_spaces_in_start_line(line) * 10
            res.append(f'<span style="margin-left: {indent}px">{line}</span>')
        return mark_safe('<br>'.join(res))

    def get_message_text(self, obj):
        """Метод выводит в колонку админки текст сообщения."""
        if obj.text is None:
            json_ = ujson.loads(obj.json)
            try:
                if audio := json_.get("audio"):
                    return mark_safe("<b>Аудио</b> - " + audio["title"])
                elif location := json_.get("location"):
                    return mark_safe(f"<b>Локация</b> - {location['latitude']}, {location['longitude']}")
                elif document := json_.get("document"):
                    return mark_safe(f"<b>Документ</b> - {File.objects.get(tg_file_id=document.get('file_id')).name}")
            except Exception as e:
                logger.error(str(e))
                return json_
        if isinstance(obj.text, str):
            return obj.text[:100] + ("..." if len(obj.text) >= 50 else "")
        return "-"

    def get_mailing_or_source(self, obj):
        """Вывод в колонку идентификатора рассылки."""
        if mailing := obj.mailing:
            return f"Mailing ({mailing.pk})"
        return str(obj)

    get_message_text.short_description = "Текст"
    get_mailing_or_source.short_description = "Источник или номер рассылки"
    get_formatted_json.short_description = 'Json сообщения'

    list_per_page = 50


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Конфигурация подписчика для административной панели."""

    inlines = [SubscriberActionInline]
    search_fields = (
        "tg_chat_id",
    )
    list_display = ("__str__", "is_active", "comment", "day", "city")


@admin.register(SubscriberAction)
class SubscriberActionAdmin(admin.ModelAdmin):
    """Конфигурация действия подписчика для административной панели."""

    list_display = (
        "subscriber",
        "date_time",
        "get_colorize_action",
    )

    def get_colorize_action(self, obj):
        """Переопределяем цвет действия.

        Подписка - зеленый
        Отписка - красный
        Реактивация - синий

        """
        if obj.action == "subscribed":
            color = "green"
        elif obj.action == "unsubscribed":
            color = "red"
        else:
            color = "blue"
        return mark_safe(f"<span style='color: {color}'>{obj.get_action_display()}</span>")

    get_colorize_action.short_description = "Действие"


admin.site.register(Mailing)
admin.site.register(AdminMessage)
admin.site.register(CallbackData)
admin.site.register(Admin)

staging_level = 'dev' if settings.DEBUG else 'prod'
admin.site.site_title = f'Quran_365_bot v{settings.VERSION} {staging_level}'
admin.site.site_header = f'Quran_365_bot v{settings.VERSION} {staging_level}'
