import json

from django.contrib import admin
from django.utils.safestring import mark_safe

from bot_init.models import AdminMessage, CallbackData, Mailing, Message, Subscriber, SubscriberAction


class SubscriberActionInline(admin.StackedInline):
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
    list_display = (
        "get_mailing_or_source", "date", "message_id", "get_message_text",
    )
    search_fields = ("text", "from_user_id", "chat_id")
    list_filter = (DisplayMailingFilter,)

    def get_message_text(self, obj):
        """Метод выводит в колонку админки текст сообщения."""
        if obj.text is None:
            json_ = json.loads(obj.json)
            try:
                if audio := json_.get("audio"):
                    return mark_safe("<b>Аудио</b> - " + audio["title"])
                elif location := json_["location"]:
                    return mark_safe(f"<b>Локация</b> - {location['latitude']}, {location['longitude']}")
            except Exception:  # TODO конкретезировать ошибку
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

    list_per_page = 50


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    inlines = [SubscriberActionInline]
    search_fields = (
        "tg_chat_id",
    )
    list_display = ("__str__", "is_active", "comment", "day", "city")


@admin.register(SubscriberAction)
class SubscriberActionAdmin(admin.ModelAdmin):
    list_display = (
        "subscriber",
        "date_time",
        "get_colorize_action"
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

admin.site.site_title = "Административная панель Quran_365_bot v2.3.2"
admin.site.site_header = "Административная панель Quran_365_bot v2.3.2"
