from django.urls import path

from apps.content.views import create_content, get_ayats, get_content, send_ayats

urlpatterns = [
    path("create/", create_content),

    path("api/getContent", get_content),
    path("api/getAyats", get_ayats),
    path("api/sendAyats", send_ayats),
]
