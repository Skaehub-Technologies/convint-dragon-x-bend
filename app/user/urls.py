from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.user.views import (
    ProfileView,
    UserProfileView,
    UserRegister,
    UserView,
    VerifyEmailView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path(
        "email-verify/<str:uidb64>/<str:token>/",
        VerifyEmailView.as_view(),
        name="email-verify",
    ),
    path("profile/<user>/", UserProfileView.as_view(), name="profile"),
    path("users/", UserView.as_view(), name="users"),
    path("profiles/", ProfileView.as_view(), name="profiles"),
]
