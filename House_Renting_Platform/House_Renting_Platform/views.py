from django.shortcuts import render,redirect
from Listing.models import ListingModel
from accounts.models import User


def index(request):
    top_properties = []
    cheaper_properties ={}
    best_value_properties = []
    listed_properties = ListingModel.objects.all()
    for x in listed_properties:
         if len(top_properties) < 6:
           top_properties.append(x) 
         else:
             break   
         
    for x in listed_properties:     
         cheaper_properties[x.pk] = x.price


    best_value = sorted(cheaper_properties.items(), key=lambda item: item[1])
    best_value = dict(best_value)
    best_value = best_value.keys()

    for x in best_value:
        property_object = ListingModel.objects.get(id=x)
        if len(best_value_properties) < 6:
            best_value_properties.append(property_object)

    return render(request, 'index.html', {
            'top_properties':top_properties,
            'b_v_p':best_value_properties
            })

        
def dashboard_view(request):
    logged_user = None
    if 'userName' in request.COOKIES:
        current_user = request.COOKIES.get('userName')
        if current_user:
           try:
             logged_user = User.objects.filter(username=current_user)
           except User.DoesNotExist:
               pass
    return render(request, 'user-profile.html', {
                    'logged_user':logged_user
                    })    
 
def about_us(request):
    return render(request, 'about-us.html')   
  
def contact_us(request):
    return render(request, 'contact.html')  
   
def our_pricing(request):
    return render(request, 'pricing.html')  
   
def terms_and_conditions(request):
    return render(request, 'privacy-policy.html')     