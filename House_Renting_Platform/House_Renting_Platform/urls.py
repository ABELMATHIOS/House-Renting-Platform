from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views  # Your project-level views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage
    path('api/auth/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('payment/', include('payment_integration.urls')),  # Your payments app URLs
    path('listing/', include("Listing.urls")),
    # path('', RedirectView.as_view(url='api/auth/')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
