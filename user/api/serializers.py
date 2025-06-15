from rest_framework import serializers
from user.models import CustomerUser

class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomerUser
        fields = ('email', 'password', 'password')

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
            user = CustomerUser.objects.create_user(**validated_data)
            user.is_active = False
            user.save()
            return user
        
class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()