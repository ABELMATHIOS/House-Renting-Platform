from django.urls import path, include
from . import views

app_name = 'Listing'

urlpatterns = [
    path('/new-property', views.new_property, name='new-property' ),
    path('/listed-properties', views.listed_properties, name='listed-properties'),
    path('/view-property-details/<int:id>', views.view_property_details, name='view-property-details'),
    path('/landing', views.landing, name='landing')
]
