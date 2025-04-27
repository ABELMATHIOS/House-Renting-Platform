from django import forms
from django.forms import ModelForm
from .models import listing

class ListingForm(ModelForm):
    class Meta:
        model = listing
        fields = '__all__'