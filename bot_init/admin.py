from django.contrib import admin

from bot_init.models import Message, Subscriber, Mailing, AdminMessage, SubscriberAction

admin.site.register(Message)
admin.site.register(Subscriber)

admin.site.register(Mailing)
admin.site.register(AdminMessage)
admin.site.register(SubscriberAction)
