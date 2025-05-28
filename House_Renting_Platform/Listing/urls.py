from django.urls import path, include
from . import views

app_name = 'Listing'

urlpatterns = [
    path('', views.index, name='index' ),
    path('listing', views.home, name='home'),
    path('landing/', views.landing, name='landing')
]
