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

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/morning-contents/', views.MorningContentView.as_view()),
    path('v1/get-not-used-ayats/', views.NotUsedAyats.as_view()),
    path('v1/get-subscribers-count/', views.GetSubscribersCount.as_view()),
    path('v1/get-data-for-usage-graphic/', views.GetDataForUsageGraphic.as_view()),
    path('v1/get-ping-to-message/', views.GetPingToMessage.as_view()),
    path('v1/send-message-to-admin/', views.SendMessageToAdmin.as_view()),
] + api_docs_urls
