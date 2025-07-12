from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account.views import CustomTokenObtainPairView, TokenValidationView, register

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", register, name="register_person"),
    path("login/", CustomTokenObtainPairView.as_view(), name="loin_person"),
    path("token/validate/", TokenValidationView.as_view(), name="validate_token"),
]
