from django.contrib import admin

from apps.content.models import MorningContent, File, Ayat, Podcast, Sura


admin.site.register(MorningContent)
admin.site.register(File)
admin.site.register(Podcast)


@admin.register(Ayat)
class AyatAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'one_day_content',)


@admin.register(Sura)
class SuraAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pars_hash',)
