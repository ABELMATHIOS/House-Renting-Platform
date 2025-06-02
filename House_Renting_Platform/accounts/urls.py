from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    LogoutView,
    RequestResetEmailView,
    PasswordResetCompleteView,
)
from .views import auth_home

urlpatterns = [
    path('', auth_home, name='auth-home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('request-reset-email/', RequestResetEmailView.as_view(), name='request-reset-email'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]