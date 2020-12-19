from django.contrib import admin

from apps.content.models import MorningContent, AudioFile, Ayat, Podcast, Sura


admin.site.register(MorningContent)
admin.site.register(AudioFile)
admin.site.register(Podcast)
admin.site.register(Sura)


@admin.register(Ayat)
class AyatAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'one_day_content',)

