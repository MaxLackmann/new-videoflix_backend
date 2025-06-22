from rest_framework import serializers
from user.models import CustomerUser, EmailVerificationToken
from mailing.services.email_service import send_verification_email
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomerUser
        fields = ('email', 'password', 'repeated_password')

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
    def validate_email(self, value):
        if CustomerUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def create(self, validated_data):
        validated_data.pop('repeated_password')
        validated_data['username'] = validated_data['email']
        user = CustomerUser.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        token_obj = EmailVerificationToken.objects.create(user=user)
        send_verification_email(user.email, str(token_obj.token))
        return user

class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get("token")
        try:
            token_obj = EmailVerificationToken.objects.get(token=token)
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Ungültiger Token")

        if token_obj.is_expired():
            token_obj.delete()
            raise serializers.ValidationError("Token ist abgelaufen")

        self.token_obj = token_obj
        return attrs

    def save(self):
        user = self.token_obj.user
        user.is_active = True
        user.save()
        self.token_obj.delete()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = CustomerUser.objects.get(email=data["email"])
        except CustomerUser.DoesNotExist:
            raise serializers.ValidationError("User or password is incorrect")

        if not check_password(data["password"], user.password):
            raise serializers.ValidationError("User or password is incorrect")

        if not user.is_active:
            raise serializers.ValidationError("E-Mail-Adresse wurde noch nicht bestätigt")
        
        self.user = user
        return data

    def create(self, validated_data):
        """Erzeugt die Tokens nach erfolgreicher Validierung."""
        refresh = RefreshToken.for_user(self.user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
