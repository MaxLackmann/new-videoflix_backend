from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.api.serializers import RegisterSerializer, LoginSerializer,\
    PasswordResetSerializer, PasswordChangeSerializer
from rest_framework.permissions import AllowAny
from user.models import CustomerUser
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from django.middleware.csrf import get_token

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        POST /register/
        ----------
        Creates a new user. Returns token that can be used to authenticate in other endpoints.
        """
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user, token = serializer.save()
            return Response({
                "user": {"id": user.id, "email": user.email},
                "token": token,
            }, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Invalid email or password"},
            status=status.HTTP_400_BAD_REQUEST
        )

class ActivateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        """
        GET /activate/<uidb64>/<token>
        Activate a new user. Returns a message indicating if the account was activated successfully or not.
        Parameters:
        uidb64 (string): The user id in base64 format.
        token (string): The token used to activate the user.
        Returns:
        JSON Object with a message indicating if the account was activated successfully or not.
        Status Codes:
        200 OK - Account activated successfully.
        400 BAD REQUEST - Account activation failed.
        """
        
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
        """
        Handle user login requests.
        This method authenticates a user using the provided email and password.
        If the authentication is successful, it sets the access and refresh tokens
        as cookies in the response, along with a CSRF token.
        Parameters:
        request (Request): The HTTP request object containing login credentials.
        Returns:
        Response: A Response object containing a success message and user details
        if login is successful, or an error message if login fails.
        Status Codes:
        200 OK - Login successful, tokens set in cookies.
        400 BAD REQUEST - Invalid email or password provided.
        """

        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"detail": "Invalid email or password"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        response = Response(
            {"detail": "Login successful", "user": {"id": user.id, "username": user.username}},
            status=status.HTTP_200_OK
        )
        response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=True, samesite='None', path='/')
        response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='None', path='/')
        csrf_token = get_token(request)
        response.set_cookie('csrftoken', csrf_token, httponly=False, secure=True, samesite='None', path='/')
        return response

class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle user logout requests.
        This method blacklists the refresh token and clears both the access and refresh tokens
        from the cookies.
        Parameters:
        request (Request): The HTTP request object containing refresh token in cookies.
        Returns:
        Response: A Response object containing a success message if logout is successful, or an
        error message if logout fails.
        Status Codes:
        200 OK - Logout successful, tokens cleared from cookies.
        400 BAD REQUEST - Refresh token not found in cookies.
        """
        
        token = request.COOKIES.get('refresh_token')
        if not token:
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(token).blacklist()
        except Exception:
            pass
        response = Response({"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', '', max_age=0, httponly=True, secure=True, samesite='None', path='/')
        response.set_cookie('refresh_token', '', max_age=0, httponly=True, secure=True, samesite='None', path='/')
        return response
    
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle refresh token requests.
        This method verifies the refresh token in the request cookies, and if valid,
        returns a new access token in the response. The new access token is also set as a
        cookie in the response.
        Parameters:
        request (Request): The HTTP request object containing the refresh token in cookies.
        Returns:
        Response: A Response object containing a success message and the new access token
        if the refresh token is valid, or an error message if the refresh token is invalid.
        Status Codes:
        200 OK - Refresh token valid, new access token returned.
        400 BAD REQUEST - Refresh token not found in cookies.
        401 UNAUTHORIZED - Invalid refresh token.
        """
        
        token = request.COOKIES.get('refresh_token')
        if not token:
            return Response({"detail": "Refresh token not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_access_token = RefreshToken(token).access_token
        except TokenError:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        response = Response({"detail": "Token refreshed", "access" : str(new_access_token)}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', str(new_access_token), httponly=True,  secure=True, samesite='None', path='/')
        return response
    
class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Handle password reset requests.
        This method verifies the email address provided in the request body, and if valid,
        sends a password reset email to the user with a link to reset the password.
        Parameters:
        request (Request): The HTTP request object containing the email address in the body.
        Returns:
        Response: A Response object containing a success message if the email is valid, or an
        error message if the email is invalid.
        Status Codes:
        200 OK - Email valid, password reset email sent.
        400 BAD REQUEST - Invalid email address.
        """
        
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"detail": "An email has been sent to reset your password."}, status=status.HTTP_200_OK)
    
class PasswordConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token):
        """
        Handle password confirm requests.
        This method verifies the token and user id provided in the request URL, and if valid,
        verifies the new and confirm password provided in the request body. If the passwords
        match, the user's password is changed to the new password.
        Parameters:
        request (Request): The HTTP request object containing the new and confirm password in the body.
        uidb64 (string): The user id in base64 format.
        token (string): The token used to confirm the password change.
        Returns:
        Response: A Response object containing a success message if the password is changed successfully, or an
        error message if the token is invalid or the passwords do not match.
        Status Codes:
        200 OK - Password changed successfully.
        400 BAD REQUEST - Passwords do not match.
        401 UNAUTHORIZED - Invalid token or user.
        """
        
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