from django.db import models
from Listing.models import ListingModel
from accounts.models import User

app_name = 'Review_And_Ratings'


VALID_RATINGS={
    5.00:'5',
    4.50:'4.5',
    4.00:'4',
    3.50:'3.5',
    3.00:'3',
    2.50:'2.5',
    2.00:'2',
    1.50:'1.5',
    1.00:'1',
}


class PropertyReviewModel(models.Model):
    property_id = models.ForeignKey(ListingModel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    review_message =models.TextField(max_length=500,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.property_id} + {self.subject}'





class PropertyRatingModel(models.Model):
    property_id = models.ForeignKey(ListingModel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(null=True,choices=VALID_RATINGS)
    status = models.BooleanField(default=True)
    ip_address = models.CharField(max_length=25,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.property_id} + {self.rating}'

