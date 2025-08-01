from django.shortcuts import render,redirect
from .forms import ListingForm
from .models import ListingModel
from django.contrib import messages
from .filters import ListingFilter
import json
from django.core.serializers.json import DjangoJSONEncoder
from .recommendations import Recommendatons,is_recommended_properties_available
from decimal import Decimal
from django.db.models.fields.files import ImageFieldFile, FieldFile
from django.core.files.storage import default_storage 
from Review_And_Ratings.forms import PropertyReviewForm
from Review_And_Ratings.models import PropertyReviewModel
from accounts.models import User

def convert_cleaned_data_to_strings(cleaned_data: dict) -> dict:
    stringified_data = {}
    for key, value in cleaned_data.items():
        if value is None:
            stringified_data[key] = None
        elif isinstance(value, Decimal):
            stringified_data[key] = str(value)
        elif isinstance(value, (ImageFieldFile, FieldFile)):
            if value and hasattr(value, 'url'):
                stringified_data[key] = value.url
            elif value:
                stringified_data[key] = str(value)
            else:
                stringified_data[key] = None
        elif isinstance(value, list):
            stringified_data[key] = [
                str(item) if not isinstance(item, (dict, list)) else convert_cleaned_data_to_strings({"_temp": item}).get("_temp")
                for item in value
            ]
        elif isinstance(value, dict):
            stringified_data[key] = convert_cleaned_data_to_strings(value)
        else:
            stringified_data[key] = str(value)
    return stringified_data

def new_property(request):
    if request.method == 'POST':
     form = ListingForm(request.POST, request.FILES)
     if form.is_valid():
        submitted_form = convert_cleaned_data_to_strings(form.cleaned_data)
        request.session['submitted_form'] = submitted_form
        if 'payment_status' in request.session:
            payment_status = request.session['payment_status']
            if payment_status == 'success':
                    new_property = form.save(commit=False)
                    lat = request.POST.get('latitude')
                    lng = request.POST.get('longitude')
                    new_property.latitude = lat if lat else None
                    new_property.longitude = lng if lng else None
                
                
                    new_property.save()
                    request.session.pop('payment_status')
                    messages.success(request, "Your property is listed succesfully!!!")
                    return redirect('index')
        else:
            return redirect('payment_integration:checkout')
    else:
        if 'submitted_form' in request.session:
         form = ListingForm(initial=request.session['submitted_form'])
        else:
         form= ListingForm()
        return render(request, 'add-property.html', {
        'form': form
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
    logged_user = None
    current_reviews = PropertyReviewModel.objects.filter(property_id=id)
    if 'userName' in request.COOKIES:
        current_user = request.COOKIES.get('userName')
        if current_user:
           try:
             logged_user = User.objects.get(username=current_user)
           except User.DoesNotExist:
               pass
    current_property = ListingModel.objects.get(id=id)
    form = PropertyReviewForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.save()
            messages.success(request, "Your Review was succesfully posted!!!")
    if 1==1:
     suggested_properties = []
     query = f"{current_property.location} {current_property.city_address} {current_property.property_type} {current_property.title} {current_property.description} {current_property.price}"
     property_recommendations = Recommendatons(query, k=6)


     if property_recommendations:
        for x in property_recommendations:
            available_properties = ListingModel.objects.get(id=x)
            if current_property != available_properties:
              suggested_properties.append(available_properties)
        form= PropertyReviewForm(initial={'property_id': current_property,'user_id':logged_user})    
        return render(request, 'property-details-v4.html', {
        'current_property': current_property,
        'suggested_properties':suggested_properties,
        'form':form,
        'current_reviews':current_reviews
        })  
    form= PropertyReviewForm(initial={'property_id': current_property,'user_id':logged_user})    
    return render(request, 'property-details-v4.html', {
       'current_property': current_property,
       'form':form,
       'current_reviews':current_reviews
    })

def review_viewer(request):
    return render(request, 'my-favorites.html', {
    })