from django.urls import path, include
from . import views

app_name = 'Listing'

urlpatterns = [
    path('/new-property', views.index, name='new-property' ),
    path('/listed-properties', views.listed_properties, name='listed-properties'),
    path('/landing', views.landing, name='landing')
]
