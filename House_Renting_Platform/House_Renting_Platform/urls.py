from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views  # Your project-level views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage
    path('api/auth/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('listing/', include('Listing.urls')),  # Added trailing slash for consistency
    path('payment/', include('payment_integration.urls')),  # Your payments app URLs
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
