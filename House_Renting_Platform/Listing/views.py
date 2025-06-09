from django.shortcuts import render,redirect
from .forms import ListingForm
from .models import ListingModel


def landing(request):
    return render(request, 'Listing/landing.html', {
    })


def index(request):
    if request.method == 'POST':
     form = ListingForm(request.POST, request.FILES)
     if form.is_valid():
        new_property = form.save(commit=False)
        # new_property.save()
        return redirect('Listing:landing')
    else:
      form= ListingForm()
    return render(request, 'add-property.html', {
        'form': form,
    })



def listed_properties(request):
    listed_properties = ListingModel.objects.all()
    return render(request, 'property-halfmap-list.html', {
       'listed_properties': listed_properties,
    })


