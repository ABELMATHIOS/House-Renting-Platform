import django_filters
from .models import ListingModel

class ListingFilter(django_filters.FilterSet):
    class Meta:
        model = ListingModel
        fields = {
            'title': ['icontains'],
            'location': ['exact'],
            'price': ['lt', 'gt'],

        }
