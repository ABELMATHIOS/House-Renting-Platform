from django import forms
import django_filters
from .models import ListingModel

class ListingFilter(django_filters.FilterSet):
    class Meta:
        model = ListingModel
        fields = {
            'title': ['icontains'],
            'province':['exact'],
            'location': ['icontains'],
            'price': ['lt', 'gt'],
            'property_type':['exact']

        }
        widgets= {
            'title':forms.TextInput(attrs={'placeholder':"Type keyword....",'class':"form-control"}),

            'province':forms.Select(attrs={'class':"nice-select"}),

            'location':forms.TextInput(attrs={'placeholder':"Enter The Neighbourhood",'class':"form-control"}),
            
            'price':forms.TextInput(attrs={'placeholder':"Example value: 12345.67",'class':"form-control"}),

            'property_type':forms.Select(attrs={'class':"nice-select"}),

        }
