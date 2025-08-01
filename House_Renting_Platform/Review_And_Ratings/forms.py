from django import forms
from django.forms import ModelForm
from Review_And_Ratings.models import PropertyRatingModel,PropertyReviewModel

class PropertyReviewForm(ModelForm):
    class Meta:
        model = PropertyReviewModel
        fields = ['property_id','user_id','review_message',]





class PropertyRatingForm(ModelForm):
    class Meta:
        model = PropertyRatingModel
        fields = ['property_id','user_id','rating','status','ip_address']