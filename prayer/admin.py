from django.contrib import admin

from prayer.models import City, Day, Prayer, PrayerAtUser, PrayerAtUserGroup


admin.site.register(City)
admin.site.register(Day)
admin.site.register(Prayer)
admin.site.register(PrayerAtUser)
admin.site.register(PrayerAtUserGroup)

