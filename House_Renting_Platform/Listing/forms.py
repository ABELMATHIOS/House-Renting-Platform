from django import forms
from django.forms import ModelForm
from .models import ListingModel

class ListingForm(ModelForm):
    class Meta:
        model = ListingModel
        fields = ['title','description','city_address','zipcode','country','province','ownership_documents','location','price','bank_debt','property_type','property_status','property_condition','property_size','property_landarea','furnished','property_rooms','bedrooms','bathrooms','parking','kitchens','balcony','property_image','link']
        widgets= {
            'title':forms.TextInput(attrs={'placeholder':"Property Title",'class':"form-control"}),

            'description':forms.Textarea(attrs={'placeholder':"Your Decscription",'class':"textarea"}),

            'city_address':forms.TextInput(attrs={'placeholder':"Enter Property City or Town",'class':"form-control"}),

            'zipcode':forms.TextInput(attrs={'placeholder':"Enter property zip code",'class':"form-control"}),

            'country':forms.Select(attrs={'class':"nice-select"}),

            'province':forms.Select(attrs={'class':"nice-select"}),

            'ownership_documents':forms.Select(attrs={'class':"nice-select"}),

            'location':forms.TextInput(attrs={'placeholder':"Enter The Neighbourhood",'class':"form-control"}),
            
            'price':forms.TextInput(attrs={'placeholder':"Example value: 12345.67",'class':"form-control"}),

            'bank_debt':forms.Select(attrs={'class':"nice-select"}),

            'property_type':forms.Select(attrs={'class':"nice-select"}),

            'property_status':forms.Select(attrs={'class':"nice-select"}),

            'property_condition':forms.Select(attrs={'class':"nice-select"}),
            
            'property_size':forms.TextInput(attrs={'placeholder':"Size of the property",'class':"form-control"}),

            'property_landarea':forms.TextInput(attrs={'placeholder':"Area of the property",'class':"form-control"}),

            'furnished':forms.Select(attrs={'class':"nice-select"}),

            'property_rooms':forms.TextInput(attrs={'placeholder':"How many Rooms does the property have ?",'class':"form-control"}),

            'bedrooms':forms.TextInput(attrs={'placeholder':"How many bedrooms does the property have ?",'class':"form-control"}),

            'bathrooms':forms.TextInput(attrs={'placeholder':"How many bathrooms does the property have ?",'class':"form-control"}),

            'parking':forms.Select(attrs={'class':"nice-select"}),

            'kitchens':forms.TextInput(attrs={'placeholder':"How many kitchens does the property have ?",'class':"form-control"}),

            'balcony':forms.TextInput(attrs={'placeholder':"How many balcony does the property have ?",'class':"form-control"}),

            'property_image':forms.FileInput(attrs={'class':"ip-file"}),

            'link':forms.TextInput(attrs={'placeholder':"Youtube, vimeo url",'class':"form-control"}),

        }