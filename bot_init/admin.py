from django.contrib import admin

from bot_init.models import Message, Subscriber, Mailing, AdminMessage, SubscriberAction


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'from_user_id', 'message_id', 'chat_id', 'get_message_text', )
    search_fields = ('text', 'from_user_id', 'chat_id')

    def get_message_text(self, obj):
        if isinstance(obj.text, str):
            return obj.text[:50] + ('...' if len(obj.text) >= 50 else '')
        return '-'

    get_message_text.short_description = 'Текст'


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    search_fields = (
        'tg_chat_id',
    )
    list_display = ('__str__', 'is_active', 'comment', 'day')


admin.site.register(Mailing)
admin.site.register(AdminMessage)


@admin.register(SubscriberAction)
class SubscriberActionAdmin(admin.ModelAdmin):
    list_display = (
        'subscriber',
        'date_time',
        'action'
    )
