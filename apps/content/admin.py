from django.contrib import admin

from apps.content.models import Ayat, File, MorningContent, Podcast, Sura

admin.site.register(MorningContent)
admin.site.register(File)
admin.site.register(Podcast)


@admin.register(Ayat)
class AyatAdmin(admin.ModelAdmin):
    """Конфигурация административной панели для аятов."""

    list_display = ('__str__', 'one_day_content')


@admin.register(Sura)
class SuraAdmin(admin.ModelAdmin):
    """Конфигурация административной панели для сур."""

    list_display = ('__str__', 'pars_hash')
