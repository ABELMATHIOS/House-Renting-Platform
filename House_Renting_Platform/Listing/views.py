from django.shortcuts import render
from .forms import ListingForm

# Create your views here.
def index(request):
    form= ListingForm 
    return render(request, 'listing.html', {
        'form': form,
    })