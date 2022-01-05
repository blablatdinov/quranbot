from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('content/', include('apps.content.urls')),
    path('bot_init/', include('apps.bot_init.urls')),
    path('api/', include('apps.api.urls')),
]
