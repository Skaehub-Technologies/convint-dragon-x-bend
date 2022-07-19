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
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path(
        "email-verify/<str:uidb64>/<str:token>/",
        VerifyEmailView.as_view(),
        name="email-verify",
    ),
    path("profile/<user>/", ProfileDetailView.as_view(), name="profile"),
    path("users/", UserView.as_view(), name="users"),
    path("profiles/", ProfileListView.as_view(), name="profiles"),
]
