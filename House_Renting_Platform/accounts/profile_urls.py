# accounts/profile_urls.py
from django.urls import path
from .views import profile_view

urlpatterns = [
    path('my-profile/', profile_view, name='my-profile'),
    # Other profile-related URLs
]