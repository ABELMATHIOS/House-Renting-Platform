from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from .models import Profile

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect


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

@login_required
def my_profile_view(request):
    if request.method == "POST" and request.FILES.get("avatar"):
        avatar_file = request.FILES["avatar"]
        profile = request.user.profile  # this will now exist
        profile.avatar = avatar_file
        profile.save()
        return redirect("my-profile")

    return render(request, "dashboard.html")


# Registration
# views.py
from django.contrib.auth import login  # import this

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)

        # ✅ Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            'message': 'User created successfully',
            'username': user.username,
            'email': user.email,
            'refresh': str(refresh),
            'access': access,
        }, status=status.HTTP_201_CREATED)




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

def user_dashboard(request):
    return render(request, 'dashboard.html')        
   