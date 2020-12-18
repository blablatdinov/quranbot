from django.urls import path

from content.views import get_content, create_content, get_ayats, send_ayats

urlpatterns = [
    path("create/", create_content),

    path("api/getContent", get_content),
    path("api/getAyats", get_ayats),
    path("api/sendAyats", send_ayats),
]
