from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.users.views import UserRegister
from app.users import views

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path(
        "",
        views.PasswordReset.as_view(),
        name="request-password-reset",
    ),
    path(
        "password-reset/<str:encoded_pk>/<str:token>/",
        views.ResetPasswordAPI.as_view(),
        name="reset-password",
    ),
]
