from django.contrib import admin

from apps.prayer.models import City, Day, Prayer, PrayerAtUser, PrayerAtUserGroup

admin.site.register(City)
admin.site.register(Day)
admin.site.register(Prayer)
admin.site.register(PrayerAtUserGroup)


@admin.register(PrayerAtUser)
class PrayerAtUserAdmin(admin.ModelAdmin):
    """Настройки админки для модели намаза пользователя."""

    list_display = ("__str__", "is_read")
