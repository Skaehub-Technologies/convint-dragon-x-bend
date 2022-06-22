from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.user.views import UserRegister

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password-reset')),
]
