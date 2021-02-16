from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.views import AyatViewSet, PodcastViewSet, PrayerAtUserViewSet

router = DefaultRouter()
router.register(r"getAyat", AyatViewSet)
router.register(r"getPodcast", PodcastViewSet)
router.register(r"getPrayerAtUser", PrayerAtUserViewSet)

urlpatterns = [
    path("v1/", include(router.urls))
]