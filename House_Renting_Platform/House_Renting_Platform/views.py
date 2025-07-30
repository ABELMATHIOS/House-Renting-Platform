from django.shortcuts import render,redirect


def index(request):
    return render(request, 'index.html', {
    })

        
def dashboard_view(request):
    return render(request, 'dashboard.html')    
 
def about_us(request):
    return render(request, 'about-us.html')   
  
def contact_us(request):
    return render(request, 'contact.html')     