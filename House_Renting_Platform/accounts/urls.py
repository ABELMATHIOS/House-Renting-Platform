from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    profile_view,
    profile_api,
    RegisterView,
    LogoutView,
    RequestResetEmailView,
    PasswordResetCompleteView,
    property_details,
    index_view,
)
from .views import CustomTokenObtainPairView

urlpatterns = [
    # API endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # Profile paths
    path('my-profile/', profile_view, name='my-profile'),  # HTML view
    path('api/my-profile/', profile_api, name='api-my-profile'),  # API endpoint
    
    # Property paths
    path('property-details/', property_details, name='property-details'),
    
    # Password reset flows
    path('request-reset-email/', RequestResetEmailView.as_view(), name='request-reset-email'),
    path('reset-password-confirm/', 
         TemplateView.as_view(template_name='accounts/reset_password_confirm.html'), 
         name='password-reset-confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    
    # Root paths (keep these last)
    path('index/', TemplateView.as_view(template_name='accounts/index.html'), name='home'),
    path('', index_view, name='index'),  # Single, unambiguous root path
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)