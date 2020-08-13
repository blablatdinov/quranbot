import json

from django.contrib import admin

from bot_init.models import Message, Subscriber, Mailing, AdminMessage, SubscriberAction, CallbackData


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('get_mailing_or_source', 'date', 'from_user_id', 'message_id', 'chat_id', 'get_message_text', )
    search_fields = ('text', 'from_user_id', 'chat_id')

    def get_message_text(self, obj):
        if obj.text is None:
            json_ = json.loads(obj.json)
            if audio := json_['audio']:
                return 'Аудио - ' + audio['title']
        if isinstance(obj.text, str):
            return obj.text[:50] + ('...' if len(obj.text) >= 50 else '')
        return '-'

    def get_mailing_or_source(self, obj):
        if mailing := obj.mailing:
            return f'Mailing ({mailing.pk})'
        return str(obj)

    get_message_text.short_description = 'Текст'


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
        'action'
    )


admin.site.register(Mailing)
admin.site.register(AdminMessage)
admin.site.register(CallbackData)
