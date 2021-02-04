from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api.views import AyatViewSet


router = DefaultRouter()
router.register(r"getSura", AyatViewSet)

urlpatterns = [
    path("v1/", include(router.urls))
]