from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.api.serializers import RegisterSerializer, VerifyEmailSerializer \
    ,LoginSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": sum(serializer.errors.values(), [])}, status=status.HTTP_400_BAD_REQUEST)

    
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("VerifyEmailView POST body:", request.data)
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.save()
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({"detail": sum(serializer.errors.values(), [])}, status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.save()
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({"detail": sum(serializer.errors.values(), [])}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset email sent if user exists"}, status=status.HTTP_200_OK)
        return Response({"detail": sum(serializer.errors.values(), [])}, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response({"detail": sum(serializer.errors.values(), [])}, status=status.HTTP_400_BAD_REQUEST)