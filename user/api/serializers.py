from rest_framework import serializers
from user.models import CustomerUser
from mailing.services.email_service import send_verification_email, send_password_reset_email
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class RegisterSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)
    privacy_policy = serializers.CharField(write_only=True)
    class Meta:
        model = CustomerUser
        fields = ('id','email', 'password', 'confirmed_password', 'privacy_policy')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def validate_email(self, value):
        if CustomerUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def create(self, validated_data):
        validated_data.pop('confirmed_password')
        validated_data.pop('privacy_policy')
        validated_data['username'] = validated_data['email']
        user = CustomerUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        refresh = RefreshToken.for_user(user)
        activation_token = str(refresh.access_token)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        send_verification_email(user.email, uid, activation_token)
        return user, activation_token
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = CustomerUser.objects.get(email=data['email'])
        except CustomerUser.DoesNotExist:
            raise serializers.ValidationError("user does not exist")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("password")
        if not user.is_active:
            raise serializers.ValidationError("Account is not activated")
        return {'user': user}

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomerUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email does not exist')
        return value
    
    def save(self):
        user = CustomerUser.objects.get(email=self.validated_data['email'])
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = str(RefreshToken.for_user(user).access_token)
        send_password_reset_email(user.email, uid, token)

class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data