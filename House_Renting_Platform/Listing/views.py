from django.shortcuts import render,redirect
from .forms import ListingForm
from .models import ListingModel
from django.contrib import messages
from .filters import ListingFilter


def landing(request):
    return render(request, 'Listing/landing.html', {
    })


def new_property(request):
    if request.method == 'POST':
     form = ListingForm(request.POST, request.FILES)
     if form.is_valid():
        new_property = form.save(commit=False)
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
    return render(request, 'property-halfmap-list.html', {
       'filter': listing_filter,
    })

def view_property_details(request, id):
    current_property = ListingModel.objects.get(id=id)
    return render(request, 'property-details-v4.html', {
       'current_property': current_property,
    })

 
