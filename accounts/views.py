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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render


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

# Registration
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Received registration data:", request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
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

            frontend_url = f"http://localhost:3000/reset-password-confirm?uid={uid}&token={token}"  # customize this
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