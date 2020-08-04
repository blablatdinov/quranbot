from django.contrib import admin

from content.models import MorningContent, AudioFile, Ayat, Podcast


admin.site.register(MorningContent)
admin.site.register(AudioFile)
admin.site.register(Ayat)
admin.site.register(Podcast)
