import json

from django.contrib import admin
from django.utils.safestring import mark_safe

from bot_init.models import Message, Subscriber, Mailing, AdminMessage, SubscriberAction, CallbackData


class DisplayMailingFilter(admin.SimpleListFilter):
    """Фильтр позволяет отключить отображение рассылок в административной панели"""
    title = 'Отображать сообщения'
    parameter_name = 'hz'

    def lookups(self, request, model_admin):
        return [('without_mailings', 'Без рассылок')]

    def queryset(self, request, queryset):
        if self.value() == 'without_mailings':
            return queryset.filter(mailing__isnull=True)
        return queryset


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'get_mailing_or_source', 'date', 'message_id', 'get_message_text',
    )
    search_fields = ('text', 'from_user_id', 'chat_id')
    list_filter = (DisplayMailingFilter,)

    def get_message_text(self, obj):
        if obj.text is None:
            json_ = json.loads(obj.json)
            try:
                if audio := json_.get('audio'):
                    return mark_safe('<b>Аудио</b> - ' + audio['title'])
                elif location := json_['location']:
                    return mark_safe(f"<b>Локация</b> - {location['latitude']}, {location['longitude']}")
            except Exception:
                return json_
        if isinstance(obj.text, str):
            return obj.text[:100] + ('...' if len(obj.text) >= 50 else '')
        return '-'

    def get_mailing_or_source(self, obj):
        if mailing := obj.mailing:
            return f'Mailing ({mailing.pk})'
        return str(obj)

    get_message_text.short_description = 'Текст'
    get_mailing_or_source.short_description = 'Источник или номер рассылки'

    list_per_page = 50


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    search_fields = (
        'tg_chat_id',
    )
    list_display = ('__str__', 'is_active', 'comment', 'day', 'city')


@admin.register(SubscriberAction)
class SubscriberActionAdmin(admin.ModelAdmin):
    list_display = (
        'subscriber',
        'date_time',
        'get_colorize_action'
    )

    def get_colorize_action(self, obj):
        action = obj.action
        if obj.action == 'subscribed':
            color = 'green'
        elif obj.action == 'unsubscribed':
            color = 'red'
        else:
            color = 'blue'
        return mark_safe(f"<span style='color: {color}'>{obj.get_action_display()}</span>")

    get_colorize_action.short_description = 'Действие'


admin.site.register(Mailing)
admin.site.register(AdminMessage)
admin.site.register(CallbackData)

admin.site.site_title = 'Административная панель Quran_365_bot v1.23'
admin.site.site_header = 'Административная панель Quran_365_bot v1.23'
