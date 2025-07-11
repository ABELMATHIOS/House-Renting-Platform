# Django imports for authentication and user management
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail

# Logging setup
import logging
logger = logging.getLogger(__name__)

# DRF imports for API views and authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.decorators import api_view, permission_classes

# Other utility imports
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# View for home page - renders basic template
def home(request):
    return render(request, 'accounts/index.html')

# API endpoint listing all available authentication endpoints
@api_view(['GET'])
def auth_home(request):
    endpoints = {
        'register': '/api/auth/register/',
        'login': '/api/auth/login/',
        'refresh': '/api/auth/refresh/',
        'logout': '/api/auth/logout/',
        'password_reset': '/api/auth/request-reset-email/',
        'password_reset_confirm': '/api/auth/password-reset-complete/',
    }
    return Response(endpoints)

def index_view(request):
    return render(request, 'index.html')

# View for authenticated user's profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    return Response({
        'username': request.user.username,
        'email': request.user.email
    })
    
@login_required
def profile_view(request):
    return render(request, 'my-profile.html', {
        'username': request.user.username,
        'email': request.user.email 
    })

# View for property details page
def property_details(request):
    return render(request, 'property-details-v4.html')

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# User registration view
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request):
        # Data validation
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()
        email = request.data.get('email', '').strip()

        # Validate required fields
        if not all([username, password, email]):
            return Response(
                {'error': 'All fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {'error': 'Enter a valid email address'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if username exists
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if email exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already registered'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Password strength check (basic example)
        if len(password) < 8:
            return Response(
                {'error': 'Password must be at least 8 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'User created successfully',
                'username': user.username,
                'email': user.email,
                'access': access_token,
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# User logout view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import logging

logger = logging.getLogger(__name__)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            
            # Always return success and let frontend handle redirect
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except TokenError as e:
                    logger.warning(f"Token blacklist error: {e}")

            return Response({
                "message": "Logout successful",
                "redirect_url": "/"  # Explicit root URL
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return Response({
                "error": str(e),
                "redirect_url": "/"  # Still provide redirect on error
            }, status=status.HTTP_400_BAD_REQUEST)
     
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Password reset request view
class RequestResetEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            # Generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            
            # Create reset link
            frontend_url = f"http://localhost:8000/api/auth/index/?uid={uid}&token={token}"

            # Send email with reset link
            send_mail(
                "Reset Your Password",
                f"Click the link to reset your password: {frontend_url}",
                "noreply@yourdomain.com",
                [email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link sent"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User with that email does not exist"}, status=status.HTTP_404_NOT_FOUND)

# Password reset completion view
class PasswordResetCompleteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Get data from request
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            # Decode user ID and get user
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            # Verify token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

        except Exception:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)