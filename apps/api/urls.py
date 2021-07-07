from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.api.api_docs import api_docs_urls
from apps.api import views

router = DefaultRouter()
router.register(r'ayats', views.AyatViewSet)
# router.register(r'getPodcast', views.PodcastViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/morning-contents/', views.MorningContentView.as_view()),
    # path('v1/getPrayerTime/', views.PrayerTimeView.as_view()),
    # path('v1/getAyat/', views.AyatAPIView.as_view()),
    # path('v1/getAyat/<int:pk>/', views.AyatDetailView.as_view()),
    path('v1/get-not-used-ayats/', views.NotUsedAyats.as_view()),
    # path('v1/setPrayerStatus/', views.PrayerTimeView.as_view()),
] + api_docs_urls
