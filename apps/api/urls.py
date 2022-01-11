from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.api import views
from apps.api.api_docs import api_docs_urls

router = DefaultRouter()
router.register(r'content/ayats', views.AyatViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('v1/content/morning-contents/', views.MorningContentView.as_view()),
    path('v1/content/get-not-used-ayats/', views.NotUsedAyats.as_view()),

    path('v1/bot/get-data-for-usage-graphic/', views.GetDataForUsageGraphic.as_view()),

    path('v1/bot/get-subscribers-count/', views.GetSubscribersCount.as_view()),
    path('v1/bot/get-ping-to-message/', views.GetPingToMessage.as_view()),
    path('v1/bot/send-message-to-admin/', views.SendMessageToAdmin.as_view()),
    path('v1/bot/mailings/<int:pk>/', views.MailingDetail.as_view()),
    path('v1/bot/mailings/', views.Mailings.as_view()),
    path('v1/bot/messages/', views.MessagesView.as_view()),
]

urlpatterns += api_docs_urls
