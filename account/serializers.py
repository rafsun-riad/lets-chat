from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Account


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ["groups", "user_permissions"]
        # fields = '__all__'
        extra_kwargs = {
            "password": {"write_only": True},
            # 'username': {'read_only': True},
        }

    def validate_email(self, value):
        if Account.objects.filter(email=value).exists():
            raise ValidationError({"error": "This email is already registered."})
        return value

    def create(self, validated_data):
        # Hash the password
        validated_data["password"] = make_password(validated_data["password"])
        return Account.objects.create(**validated_data)

    def to_representation(self, instance):
        """Customize the serialized output."""
        representation = super().to_representation(instance)
        # Remove the password field from the output
        representation.pop("password", None)
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # Exclude the password field for security
        exclude = ("password", "groups", "user_permissions")


class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        # Check the password
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        # Generate tokens using Simple JWT
        refresh = RefreshToken.for_user(user)

        user_data = UserSerializer(user).data

        # If authentication is successful, get the tokens
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data,
        }

        return data
