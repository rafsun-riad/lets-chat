from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


# Create your views here.
@extend_schema(
    request=inline_serializer(
        name="UserRegistrationRequest",
        fields={
            "first_name": serializers.CharField(required=False, allow_blank=True),
            "last_name": serializers.CharField(required=False, allow_blank=True),
            "email": serializers.EmailField(required=True),
            "password": serializers.CharField(write_only=True, required=True),
            "phone": serializers.CharField(required=True, allow_blank=True),
        },
    ),
    responses={
        201: OpenApiResponse(description="Person registered successfully"),
        400: OpenApiResponse(description="Validation error"),
    },
    summary="Register new user",
    description="Registers a new user by providing email, password and phone number.",
)
@api_view(["POST"])
def register(request):
    if request.method == "POST":
        data = request.data
        data["username"] = data["email"]
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Person registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class TokenValidationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user

        # Generate tokens using Simple JWT
        refresh = RefreshToken.for_user(user)

        user_data = UserSerializer(user).data
        # Prepare the data to be returned
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data,
        }

        return Response(data)
