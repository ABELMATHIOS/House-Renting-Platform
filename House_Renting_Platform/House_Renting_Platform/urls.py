from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # API endpoints
    path('api/auth/', include('accounts.urls')),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='index.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # App routes
    path('listing/', include("Listing.urls")),
    path('profile/', include('accounts.profile_urls')),  # See note below
    
    # Core routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    
    # Root redirect (only one!)
    path('', views.index, name='index'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)