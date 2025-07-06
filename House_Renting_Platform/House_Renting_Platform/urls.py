from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index' ),
    path('login/', auth_views.LoginView.as_view(template_name='index.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/auth/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('listing/', include("Listing.urls")),
    path('', RedirectView.as_view(url='api/auth/')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)