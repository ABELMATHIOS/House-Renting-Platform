from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from .models import Profile

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import login  # import this
from django.http import JsonResponse

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


def home(request):
    return render(request, 'accounts/index.html')

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

from django.contrib.auth.decorators import login_required

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def my_profile_view(request):
    if not request.user.is_authenticated:
        if request.headers.get('Authorization'):
            # JWT authentication will handle this
            pass
        else:
            return JsonResponse(
                {'error': 'Unauthorized'}, 
                status=401
            )
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'username': request.user.username,
            'email': request.user.email
        })
    
    return render(request, 'my-profile.html')

def property_details(request):
    return render(request, 'property-details-v4.html')

# Registration
User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

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

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # You could log the user in sessionally if needed
            # login(request, user)  # Uncomment if using session auth alongside JWT

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



from rest_framework_simplejwt.exceptions import TokenError

import logging
logger = logging.getLogger(__name__)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            logger.warning(f"Logout: Token error - {e}")
            return Response({"message": "Token already blacklisted or invalid."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"Logout failed: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



# Request password reset via email
class RequestResetEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            
            frontend_url = f"http://localhost:8000/api/auth/index/?uid={uid}&token={token}"

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

# Complete password reset
class PasswordResetCompleteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

        except Exception:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)