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
        """
        Check that the given password and confirmed_password are equal.
        :param data: The validated data from the serializer
        :raises serializers.ValidationError: If password and confirmed_password do not match
        :return: The validated data if the passwords match
        """
        
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def validate_email(self, value):
        """
        Check if the given email already exists in the database. If it does,
        raise a serializers.ValidationError with the message 'Email already exists'.
        Otherwise, return the given email.
        """
        
        if CustomerUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def create(self, validated_data):
        """
        Create a new user with the given validated_data. The user will be
        inactive and a verification email will be sent to the user. The
        user's username is set to be the same as the email. The password
        is set to the given password. The activation token is returned
        along with the created user.
        :param validated_data: The validated data from the serializer
        :return: The created user and the activation token
        """
        
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
        """
        Validate the login credentials provided in the data.
        This method checks if a user with the given email exists, verifies the 
        provided password against the stored password, and ensures that the 
        account is activated.
        :param data: A dictionary containing the login email and password.
        :raises serializers.ValidationError: If the user does not exist, the 
        password is incorrect, or the account is not activated.
        :return: A dictionary containing the authenticated user.
        """

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
        """
        Validate the email address provided in the data.
        This method checks if a user with the given email address exists in the database.
        If the email address does not exist, a serializers.ValidationError is raised.
        :param value: The email address to validate.
        :raises serializers.ValidationError: If the email address does not exist.
        :return: The validated email address.
        """
        
        if not CustomerUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email does not exist')
        return value
    
    def save(self):
        """
        Save method to initiate the password reset process.
        This method retrieves the user associated with the validated email,
        generates a unique user ID and a password reset token, and sends a 
        password reset email to the user.
        """

        user = CustomerUser.objects.get(email=self.validated_data['email'])
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = str(RefreshToken.for_user(user).access_token)
        send_password_reset_email(user.email, uid, token)

class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the new and confirm password provided in the data.
        This method checks if the new and confirm password are equal.
        If the passwords do not match, a serializers.ValidationError is raised.
        :param data: A dictionary containing the new and confirm password.
        :raises serializers.ValidationError: If the passwords do not match.
        :return: The validated data if the passwords match.
        """
        
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return data