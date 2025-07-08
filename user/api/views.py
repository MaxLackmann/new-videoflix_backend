from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.api.serializers import RegisterSerializer, LoginSerializer,\
    PasswordResetSerializer, PasswordChangeSerializer
from rest_framework.permissions import AllowAny
from user.models import CustomerUser
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            user, token = serializer.save()
            return Response({
                "user": {"id": user.id, "email": user.email},
                "token": token,
            }, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class ActivateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomerUser.objects.get(pk=uid)
            access_token = AccessToken(token)

            if str(user.pk) != str(access_token['user_id']):
                raise Exception

            if not user.is_active:
                user.is_active = True
                user.save()

                return Response({"detail": "Account successfully activated."}, status=status.HTTP_200_OK)
            return Response({"detail": "Account already activated."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Account activation failed."}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        response = Response(
            {"detail": "Login successful", "user": {"id": user.id, "username": user.username}},
            status=status.HTTP_200_OK
        )
        response.set_cookie('access_token', str(refresh.access_token), httponly=False, secure=True, samesite='None')
        response.set_cookie('refresh_token', str(refresh), httponly=False, secure=True, samesite='None')
        return response

class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print(f"LogoutView Cookies: {request.COOKIES}")
        token = request.COOKIES.get('refresh_token')
        if not token:
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(token).blacklist()
        except Exception:
            pass
        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', '', max_age=0, httponly=False, secure=True, samesite='None')
        response.set_cookie('refresh_token', '', max_age=0, httponly=False, secure=True, samesite='None')
        return response
    
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token = request.COOKIES.get('refresh_token')
        if not token:
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_access_token = RefreshToken(token).access_token
        except TokenError:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        response = Response({"detail": "Token refreshed", "access" : str(new_access_token)}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', str(new_access_token), httponly=True)
        return response
    
class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"detail": "An email has been sent to reset your password."}, status=status.HTTP_200_OK)
    
class PasswordConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token):
        serializer = PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uid  = urlsafe_base64_decode(uidb64).decode()
            user = CustomerUser.objects.get(pk=uid)
        except Exception:
            return Response(
                {"detail": "Invalid token or user"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"detail": "Your Password has been successfully reset."},
            status=status.HTTP_200_OK
        )