from django.shortcuts import render,redirect
from .forms import ListingForm
from .models import ListingModel
from django.contrib import messages
from .filters import ListingFilter
import json
from django.core.serializers.json import DjangoJSONEncoder
from .recommendations import Recommendatons

def landing(request):
    return render(request, 'Listing/landing.html', {
    })


def new_property(request):
    if request.method == 'POST':
     form = ListingForm(request.POST, request.FILES)
     if form.is_valid():
        new_property = form.save(commit=False)
        # Get latitude and longitude from the POST data
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        
         # Assign latitude and longitude to the property
        new_property.latitude = lat if lat else None
        new_property.longitude = lng if lng else None

        new_property.save()
        messages.success(request, "Your property is listed succesfully!!!")
        return redirect('index')
    else:
      form= ListingForm()
    return render(request, 'add-property.html', {
        'form': form,
    })



def listed_properties(request):
    listed_properties = ListingModel.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listed_properties)

    map_properties = listing_filter.qs.values('id', 'title', 'latitude', 'longitude')

    return render(request, 'property-halfmap-list.html', {
        'filter': listing_filter,
        'map_properties': json.dumps(list(map_properties), cls=DjangoJSONEncoder),  # JSON encode properly
    })


def view_property_details(request, id):
    suggested_properties = []
    current_property = ListingModel.objects.get(id=id)
    query = f"{current_property.location} {current_property.city_address} {current_property.property_type} {current_property.title} {current_property.description} {current_property.price}"
    property_recommendations = Recommendatons(query, k=6)

    for x in property_recommendations:
       listed_properties = ListingModel.objects.get(id=x)
       suggested_properties.append(listed_properties)
       

    suggested_properties.pop(0)   
    
    
    return render(request, 'property-details-v4.html', {
       'current_property': current_property,
        'suggested_properties':suggested_properties,
    })

def review_viewer(request):
    return render(request, 'my-favorites.html', {
    })

 
