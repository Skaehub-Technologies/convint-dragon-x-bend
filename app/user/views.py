from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import generics, status, response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from app.user.models import Profile
from app.user.permissions import IsUser
from app.user.serializers import (
    ProfileSerializer,
    UserSerializer,
    VerifyEmailSerializer,
    PasswordResetSerializer,
    VerifyPasswordResetSerializer,
)

User = get_user_model()


class PasswordReset(generics.GenericAPIView):
    """
    Request for Password Reset Link.
    """

    serializer_class = PasswordResetSerializer

    def post(self, request: Request, format: str = "json") -> Response:

        serializer = self.get_serializer(
            data={"email": request.data.get("email")}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "check your email for password reset link"},
            status=status.HTTP_200_OK,
        )


class VerifyPasswordReset(generics.GenericAPIView):

    serializer_class = VerifyPasswordResetSerializer

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.get_serializer(
            data=request.data, context={"kwargs": kwargs}
        )

        serializer.is_valid(raise_exception=True)

        return response.Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )

class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
        IsUser,
    )
    serializer_class = ProfileSerializer
    lookup_field = "user"
    queryset = Profile.objects.all()
    renderer_classes = (JSONRenderer,)


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

