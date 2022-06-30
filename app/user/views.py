from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app.user.serializers import UserSerializer, VerifyEmailSerializer

User = get_user_model()


class UserRegister(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = UserSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def get(self, request, uidb64, token, **kwargs) -> Response:  # type: ignore
        data = {"uidb64": uidb64, "token": token}

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response("Email verified", status=status.HTTP_200_OK)
