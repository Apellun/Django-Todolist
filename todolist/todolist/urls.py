from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from bot.views import VerificationView

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/goals/', include('goals.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/bot/verify/', VerificationView.as_view(), name="tguser_verification"),
    path('api/schema/', SpectacularAPIView.as_view(api_version='v1'), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
