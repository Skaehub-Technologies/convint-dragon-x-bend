from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.user.views import PasswordReset, VerifyPasswordReset

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "password-reset/",
        PasswordReset.as_view(),
        name="password-reset",
    ),
    path(
        "verify-password-reset/<str:encoded_pk>/<str:token>/",
        VerifyPasswordReset.as_view(),
        name="verify-password-reset",
    ),
]
