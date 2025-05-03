from django.shortcuts import render,redirect
from .forms import ListingForm
from .models import ListingModel

# Create your views here.
def landing(request):
    return render(request, 'landing.html', {
    })


def index(request):
    if request.method == 'POST':
     form = ListingForm(request.POST, request.FILES)
     if form.is_valid():
        new_property = form.save(commit=False)
        new_property.save()
        return redirect('landing/')
    else:
      form= ListingForm()
    return render(request, 'listing.html', {
        'form': form,
    })



def home(request):
    ava_properties = ListingModel.objects.all()
    return render(request, 'home.html', {
       'ava_properties': ava_properties,
    })


