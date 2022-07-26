from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.user.models import Profile
from app.user.token import account_activation_token
from app.user.utils import create_email_data, generate_token, send_email
from app.user.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=20,
        min_length=8,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    class Meta:
        model = User
        fields = ("email", "username", "password")

    def create(self, validated_data: Any) -> Any:
        user = User.objects.create_user(**validated_data)
        user.save()
        Profile.objects.create(user=user)
        token_info = generate_token(user)
        request = self.context.get("request")
        email_data = create_email_data(
            request,
            user,
            encoded_pk=user,
            token=token_info,
            url="email-verify",
            subject="Verify your email!",
        )
        send_email("email_verification.html", email_data)
        return user


class VerifyEmailSerializer(serializers.Serializer):
    encoded_pk = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        fields = ("encoded_pk", "token")

    def validate(self, data: Any) -> Any:
        user = None
        try:
            user_id = force_str(urlsafe_base64_decode(data.get("encoded_pk")))
            user = User.objects.get(pk=user_id)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(
                "Invalid user id", code="invalid_code"
            )

        token = data.get("token")
        if user and account_activation_token.check_token(user, token):
            return data

        raise serializers.ValidationError(
            "Invalid or expired token", code="invalid_token"
        )

    def save(self, **kwargs: Any) -> Any:
        user_id = force_str(
            urlsafe_base64_decode(self.validated_data.get("encoded_pk"))
        )
        user = User.objects.get(pk=user_id)
        user.is_verified = True
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Profile
        fields = ("username", "bio", "image")

    def update(self, instance: Any, validated_data: Any) -> Any:
        instance.bio = validated_data.get("bio", instance.bio)
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    class Meta:
        fields = ["email"]

    def validate(self, attrs: Any) -> Any:
        user = User.objects.filter(email=attrs["email"]).first()
        if user:
            token_info = generate_token(user)
            request = self.context.get("request")
            email_data = create_email_data(
                request,
                user,
                encoded_pk=user,
                token=token_info,
                url="verify-password-reset",
                subject="Password Reset!",
            )
            send_email("password_reset.html", email_data)

        return super().validate(attrs)


class VerifyPasswordResetSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    class Meta:

        fields = ["password", "encoded_pk", "token"]

    def validate(self, data: Any) -> Any:

        password = data.get("password")
        url_kwargs = self.context.get("kwargs")
        token = url_kwargs.get("token")  # type: ignore[union-attr]
        encoded_pk = url_kwargs.get("encoded_pk")  # type: ignore[union-attr]

        try:

            pk = urlsafe_base64_decode(encoded_pk).decode()
            user = User.objects.get(pk=pk)

        except Exception:
            raise serializers.ValidationError(
                {"detail": "The encoded_pk is invalid"}
            )

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError(
                {"detail": "The reset token is invalid"}
            )

        user.set_password(password)
        user.save()
        return data
