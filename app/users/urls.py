from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.users.views import PasswordReset, ResetPasswordAPI

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "password-reset/",
        PasswordReset.as_view(),
        name="request-password-reset",
    ),
    path(
        "request-password-reset/<str:encoded_pk>/<str:token>/",
        ResetPasswordAPI.as_view(),
        name="reset-password",
    ),
]
