from django.db import models
class listing(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    parking = models.BooleanField(default=False)
    property_type = models.CharField(max_length=50, choices=[('Apartment', 'Apartment'), ('House', 'House'), ('Condo', 'Condo')], blank=True)
    property_size = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    furnished = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    def __str__(self): 
        return self.title
    
    