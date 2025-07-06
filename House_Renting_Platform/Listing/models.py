from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class ListingModel(models.Model):
    ETHIOPIA="ETH"
    KENYA="KEN"
    ADDIS_ABEBA="Addis Abeba"
    AFAR="Afar"
    AMHARA="Amhara"
    BENINGSHANGUL_GUMUZ="Benishangul Gumuz"
    CENTRAL_ETHIOPIA="Central Ethiopia"
    GAMBELA="Gambella"
    HARARI="Harari"
    OROMIA="Oromia"
    SIDAMA="Sidama"
    SOMALI_REGION="Somali Region"
    SOUTH_ETHIOPIA="South Ethiopia"
    SW_ETHIOPIA="South West Ethiopia"
    TIGRAY="Tigray"
    DC="Digital Certificate of Land Ownership"
    LO="Lease Ownership"
    CO="Cadester Ownership"
    YES="Yes"
    NO="No"
    APARTMENT="Apartment"
    BARE_LAND="Bare Land"
    BUSINESS_SHOP="Business Shop"
    COMMERCIAL_LAND="Commercial Land"
    CONDOMINIUM="Condominium"
    LAND_FOR_PLOT="Land for Plot"
    OFFICE="Office"
    STUDIO="Studio"
    TOWNHOUSE="Townhouse"
    VILLA="Villa"
    FOR_RENT="For Rent"
    FOR_SALE="For Sale"
    NEW_BUILT="Newly Built"
    OLD_BUILT="!0+ Years Ago"
    AV="Available"
    NOT_AV="Not Available"


    COUNTRY={
        ETHIOPIA:"Ethiopia",
        KENYA:"Kenya"
    }

    PROVINCE={
        ADDIS_ABEBA:"Addis Abeba",
        AFAR:"Afar",
        AMHARA:"Amhara",
        BENINGSHANGUL_GUMUZ:"Benishangul Gumuz",
        CENTRAL_ETHIOPIA:"Central Ethiopia",
        GAMBELA:"Gambella",
        HARARI:"Harari",
        OROMIA:"Oromia",
        SIDAMA:"Sidama",
        SOMALI_REGION:"Somali Region",
        SOUTH_ETHIOPIA:"South Ethiopia",
        SW_ETHIOPIA:"South West Ethiopia",
        TIGRAY:"Tigray"
    }

    OWNERSHIP_DOCUMENTS={
        DC:"Digital Certificate of Land Ownership",
        LO:"Lease Ownership",
        CO:"Cadester Ownership"
    }

    YESNO={
        YES:"Yes",
        NO:"No"
    }

    PROPERTY_TYPE={
        APARTMENT:"Apartment",
        BARE_LAND:"Bare Land",
        BUSINESS_SHOP:"Business Shop",
        COMMERCIAL_LAND:"Commercial Land",
        CONDOMINIUM:"Condominium",
        LAND_FOR_PLOT:"Land for Plot",
        OFFICE:"Office",
        STUDIO:"Studio",
        TOWNHOUSE:"Townhouse",
        VILLA:"Villa",
    }
    PROPERTY_STATUS={
        FOR_RENT:"For Rent",
        FOR_SALE:"For Sale"
    }

    PROPERTY_CONDITION={
        NEW_BUILT:"Newly Built",
        OLD_BUILT:"10+ Years Ago"
    }

    AVAILABLE={
        AV:"Available",
        NOT_AV:"Not Available"
    }

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=False)
    city_address = models.CharField(max_length=255,null=True, blank=False)
    zipcode = models.IntegerField(max_length=10,null=True, blank=False)
    country = models.CharField(max_length=3,choices=COUNTRY, default=ETHIOPIA)
    province = models.CharField(max_length=255,choices=PROVINCE,default=ADDIS_ABEBA)
    ownership_documents = models.CharField(max_length=255,choices=OWNERSHIP_DOCUMENTS,default=DC)
    location = models.CharField(max_length=255,null=True, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bank_debt=models.CharField(blank=True,choices=YESNO,default=NO)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE,default=APARTMENT)
    property_status= models.CharField(max_length=255,choices=PROPERTY_STATUS,default=FOR_RENT)
    property_condition=models.CharField(max_length=255,choices=PROPERTY_CONDITION,default=OLD_BUILT)
    property_size = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    property_landarea = models.DecimalField(max_digits=10, decimal_places=2,blank=False,null=True)
    furnished = models.CharField(max_length=3,choices=YESNO,default=NO)
    property_rooms = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    parking = models.CharField(max_length=155,choices=AVAILABLE,default=NOT_AV)
    kitchens=models.IntegerField(null=True, blank=True)
    balcony = models.IntegerField(null=True, blank=True)
    property_image = models.ImageField(default="default.png", blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True,null=True)
    homeowner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    is_approved = models.BooleanField(default=False)
    available_from = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_property_status_display()}"
    
class Booking(models.Model):
    PENDING = 'P'
    CONFIRMED = 'C'
    CANCELLED = 'X'
    COMPLETED = 'D'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
    ]
    
    listing = models.ForeignKey(ListingModel, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Calculate duration and amount if not set
        if not self.total_amount:
            duration = (self.end_date - self.start_date).days
            self.total_amount = duration * self.listing.price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.listing.title}"

class Revenue(models.Model):
    UNPAID = 'U'
    PAID = 'P'
    PROCESSING = 'R'
    
    PAYMENT_STATUS = [
        (UNPAID, 'Unpaid'),
        (PAID, 'Paid'),
        (PROCESSING, 'Processing'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='revenue')
    homeowner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revenues')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    homeowner_share = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=UNPAID)
    payment_date = models.DateField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.booking.total_amount
        if not self.commission:
            # Example: 10% commission
            self.commission = self.amount * Decimal('0.10')
        if not self.homeowner_share:
            self.homeowner_share = self.amount - self.commission
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Revenue #{self.id} - {self.homeowner.username}"