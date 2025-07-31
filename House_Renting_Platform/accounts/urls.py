from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    LogoutView,
    RequestResetEmailView,
    PasswordResetCompleteView,
    user_dashboard,
    my_profile_view,  # Added import for my_profile_view
)
from django.urls import get_resolver
from django.views.generic import TemplateView

from django.http import HttpResponseRedirect

app_name = 'profile'

def auth_root_redirect(request):
    # Example: redirect to your index page under /api/auth/index/
    return HttpResponseRedirect('index/')

urlpatterns = [
 #   path('', auth_root_redirect, name='auth-root'),
    path("", my_profile_view, name="my-profile"),  
  #  path('index/', TemplateView.as_view(template_name='accounts/index.html'), name='home'),
    path("my-profile/", my_profile_view, name="my-profile"),
  #  path('property-details/', views.property_details, name='property-details'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('request-reset-email/', RequestResetEmailView.as_view(), name='request-reset-email'),
    path('reset-password-confirm/', TemplateView.as_view(template_name='accounts/reset_password_confirm.html'), name='password-reset-confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('dashboard', user_dashboard , name='user-dashboard')
]
