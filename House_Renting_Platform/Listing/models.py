from django.db import models

class ListingModel(models.Model):
    ETHIOPIA="ETHIOPIA"
    KENYA="KENYA"
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
    OLD_BUILT="10+ Years Ago"
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
    zipcode = models.IntegerField(null=True, blank=False)
    country = models.CharField(max_length=20,choices=COUNTRY, default=ETHIOPIA)
    province = models.CharField(max_length=255,choices=PROVINCE,default=ADDIS_ABEBA)
    ownership_documents = models.CharField(max_length=255,choices=OWNERSHIP_DOCUMENTS,default=DC)
    location = models.CharField(max_length=255,null=True, blank=False)
    price = models.DecimalField(max_digits=15, decimal_places=2)
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
    
    def __str__(self): 
        return self.title
    
    