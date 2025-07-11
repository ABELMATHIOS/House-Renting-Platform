from django.shortcuts import render,redirect
from Review_And_Ratings.models import PropertyReviewModel,PropertyRatingModel
from Review_And_Ratings.forms import PropertyReviewForm,PropertyRatingForm
from django.contrib import messages


def new_review(request):
    if request.method == 'POST':
     form = PropertyReviewForm(request.POST, request.FILES)
     if form.is_valid():
        new_reviews = form.save(commit=False)
        new_reviews.save()
        messages.success(request, "Your review is posted succesfully!!!")
        return redirect('/')
     else:
        messages.warning(request, "Please fill out the form correctly!!!")
    else:
      form= PropertyReviewForm()
    return render(request, 'test_review&ratings.html', {
        'review_form': form,
    })





def new_rating(request):
    if request.method == 'POST':
     form = PropertyRatingForm(request.POST, request.FILES)
     if form.is_valid():
        new_ratings = form.save(commit=False)
        new_ratings.save()
        messages.success(request, "Your rating is posted succesfully!!!")
        return redirect('/')
     else:
        messages.warning(request, "Please fill out the form correctly!!!")
    else:
      form= PropertyRatingForm()
    return render(request, 'test_review&ratings.html', {
        'ratings_form': form,
    })