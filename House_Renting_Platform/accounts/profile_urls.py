# accounts/profile_urls.py
from django.urls import path
from .views import profile_view, profile_api  # Make sure profile_api is imported

urlpatterns = [
    path('my-profile/', profile_view, name='my-profile'),                   # HTML page
    path('api/my-profile/', profile_api, name='api-my-profile'),           # API endpoint
]