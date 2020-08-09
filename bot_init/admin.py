from django.contrib import admin

from bot_init.models import Message, Subscriber, Mailing, AdminMessage, SubscriberAction

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'from_user_id', 'message_id', 'chat_id', 'get_message_text', )
    search_fields = ('text', )

    def get_message_text(self, obj):
        if isinstance(obj.text, str):
            return obj.text[:50] + ('...' if len(obj.text) >= 50 else '')
        return '-'

    get_message_text.short_description = 'Текст'


admin.site.register(Subscriber)

admin.site.register(Mailing)
admin.site.register(AdminMessage)
admin.site.register(SubscriberAction)
