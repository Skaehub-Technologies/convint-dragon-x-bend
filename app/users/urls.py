from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.users.views import PasswordReset, ResetPasswordAPI, UserRegister

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", UserRegister.as_view(), name="register"),
    path("", PasswordReset.as_view(), name="request-password-reset"),
    path(
        "request-password-reset/<str:encoded_pk>/<str:token>/",
        ResetPasswordAPI.as_view(),
        name="reset-password",
    ),
]
