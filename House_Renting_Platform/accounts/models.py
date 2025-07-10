# Import Django's database models and built-in User model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Function to define the upload path for user avatars
def avatar_upload_path(instance, filename):
    """
    Generates upload path for user avatars in format: 
    'avatars/user_<user_id>/<filename>'
    """
    return f'avatars/user_{instance.user.id}/{filename}'

# Profile model extending Django's built-in User model
class Profile(models.Model):
    """
    User profile model with one-to-one relationship to User model.
    Extends basic user information with profile picture (avatar).
    """
    
    # One-to-one relationship with Django's User model
    # When User is deleted, their Profile is automatically deleted (CASCADE)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'  # Allows accessing profile via user.profile
    )
    
    # Avatar image field with custom upload path
    # Optional field (null=True, blank=True) - users don't have to upload an avatar
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True, 
        blank=True,
        help_text="User profile picture"
    )

    # String representation of the profile (shows username)
    def __str__(self):
        return self.user.username
