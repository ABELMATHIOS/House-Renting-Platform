from django.urls import path
from . import views
app_name = 'payment_integration'
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('success/', views.payment_success, name='payment_success'),
    path('failure/', views.payment_failure, name='payment_failure'),
]