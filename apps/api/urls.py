from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.api_docs import api_docs_urls
from apps.api.views import AyatViewSet, PodcastViewSet, PrayerTimeView

router = DefaultRouter()
router.register(r"getAyat", AyatViewSet)
router.register(r"getPodcast", PodcastViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/getPrayerTime", PrayerTimeView.as_view()),
    path("v1/setPrayerStatus", PrayerTimeView.as_view()),
] + api_docs_urls
