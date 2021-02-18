from apps.prayer.models import Prayer
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.views import AyatViewSet, PodcastViewSet, PrayerAtUserGroupViewSet

router = DefaultRouter()
router.register(r"getAyat", AyatViewSet)
router.register(r"getPodcast", PodcastViewSet)
router.register(r"getPrayerAtUser", PrayerAtUserGroupViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]