from django.urls import path
from content_gen.views import content_gen, send_content


urlpatterns = [
    path('', content_gen),
    path('/send', send_content)
]
