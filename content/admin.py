from django.contrib import admin

from content.models import MorningContent, AudioFile, Ayat, Podcast


admin.site.register(MorningContent)
admin.site.register(AudioFile)


@admin.register(Ayat)
class AyatAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'one_day_content',)


admin.site.register(Podcast)
