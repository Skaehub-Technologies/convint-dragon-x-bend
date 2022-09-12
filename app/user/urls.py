from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.user.views import (
    FollowersFollowingView,
    FollowProfile,
    LogoutView,
    PasswordReset,
    ProfileDetailView,
    ProfileListView,
    UnFollowProfile,
    UserRegister,
    UserView,
    VerifyEmailView,
    VerifyPasswordReset,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path(
        "email-verify/<str:encoded_pk>/<str:token>/",
        VerifyEmailView.as_view(),
        name="email-verify",
    ),
    path("profile/<str:user>/", ProfileDetailView.as_view(), name="profile"),
    path("users/", UserView.as_view(), name="users"),
    path("profiles/", ProfileListView.as_view(), name="profiles"),
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
    path(
        "following/<str:id>/",
        FollowersFollowingView.as_view(),
        name="following",
    ),
    path("follow/", FollowProfile.as_view(), name="follow"),
    path("unfollow/<str:id>/", UnFollowProfile.as_view(), name="unfollow"),
]
