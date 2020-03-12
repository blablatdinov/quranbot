from django.contrib import admin
from bot.models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'from_user_id', 'message_id', 'chat_id', 'text', )


class SubsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')

admin.site.register(QuranAyat)
admin.site.register(QuranOneDayContent)
admin.site.register(Subscribers, SubsAdmin)
admin.site.register(Audio)
admin.site.register(Message, MessageAdmin)

