from django.contrib import admin
from bot.models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'from_user_id', 'message_id', 'chat_id', 'text', )
    search_fields = ('text', )


class SubsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'comment', 'day')

class AudioAdmin(admin.ModelAdmin):
    search_fields = ('title', )


admin.site.register(QuranAyat)
admin.site.register(QuranOneDayContent)
admin.site.register(Subscribers, SubsAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(AdminMessage)

