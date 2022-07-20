from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from app.user.views import (
    ProfileDetailView,
    ProfileListView,
    UserRegister,
    UserView,
    VerifyEmailView,
    PasswordReset,
    VerifyPasswordReset
)


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
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
    path("profile/<str:user>/", ProfileDetailView.as_view(), name="profile"),
    path("users/", UserView.as_view(), name="users"),
    path("profiles/", ProfileListView.as_view(), name="profiles"),
]
