from django.contrib import admin

from prayer.models import City, Day, Prayer, PrayerAtUser, PrayerAtUserGroup


admin.site.register(City)
admin.site.register(Day)
admin.site.register(Prayer)
@admin.register(PrayerAtUser)
class PrayerAtUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_read')



admin.site.register(PrayerAtUserGroup)

