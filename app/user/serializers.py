from typing import Any

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView

from app.user.models import Profile
from speaksfer.settings.base import EMAIL_USER

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=20,
        min_length=8,
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("email", "username", "password")

    @staticmethod
    def send_email(user: Any) -> None:
        email_body = render_to_string(
            "email_verification.html", {"user": user}
        )
        send_mail(
            "Verify  your email!",
            email_body,
            EMAIL_USER,
            [user.email],
            fail_silently=False,
        )

    def create(self, validated_data: Any) -> Any:
        user = User.objects.create_user(**validated_data)
        self.send_email(user)

        return user


class VerifyEmailSerializer(APIView):
    def get(self, request: Request) -> Response:
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)  # type: ignore
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"email": "Successfully Activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as identifier:  # noqa F841
            return Response(
                {"error": "Activation Link is expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError as identifier:  # noqa F841
            return Response(
                {"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST
            )


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("username", "bio", "image")
        read_only_fields = "username"
