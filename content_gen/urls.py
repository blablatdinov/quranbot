from django.urls import path
from content_gen.views import content_gen


urlpatterns = [
    path('', content_gen)
]