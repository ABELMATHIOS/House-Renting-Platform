from django import forms
from django.forms import ModelForm
from .models import ListingModel

class ListingForm(ModelForm):
    class Meta:
        model = ListingModel
        fields = ['title','description','price','location','bedrooms','bathrooms','parking','property_type','property_size','furnished','available','link','property_image']