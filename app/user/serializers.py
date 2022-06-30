from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.validators import UniqueValidator

from app.user.models import Profile
from app.user.token import account_activation_token
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
    def send_email(user: Any, request: Request) -> None:

        current_site_info = get_current_site(request)
        email_body = render_to_string(
            "email_verification.html",
            {
                "user": user,
                "domain": current_site_info.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )

        send_mail(
            "Verify  your email!",
            email_body,
            EMAIL_USER,
            [user.email],
            fail_silently=False,
        )

    def create(self, validated_data: Any) -> Any:
        request = self.context.get("request")
        user = User.objects.create_user(**validated_data)
        self.send_email(user, request)  # type: ignore

        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("username", "bio", "image")
        read_only_fields = "username"


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
    uidb64 = serializers.CharField()

    class Meta:
        fields = ("token", "uidb64")

    def validate(self, data: Any) -> Any:
        user = None
        try:
            user_id = force_str(urlsafe_base64_decode(data.get("uidb64")))
            user = User.objects.get(pk=user_id)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(
                "Invalid user id", code="invalid_code"
            )

        token = data.get("token")

        if user and account_activation_token.check_token(user, token):
            user.is_verified = True
            user.save()
            return data

        raise serializers.ValidationError(
            "Invalid or expired token", code="invalid_token"
        )
