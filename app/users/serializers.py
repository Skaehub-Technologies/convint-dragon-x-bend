from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.validators import UniqueValidator

from app.users.utils import Util

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


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    class Meta:
        fields = ["email"]

    def validate(self, attrs: Any) -> Any:
        try:
            request = self.context.get("request")
            email = attrs.get("email")
            user = Util.generate_reset_token(email)

            if user:
                email_data = Util.create_reset_email(request, *user)
                Util.send_email("password_reset.html", email_data)
        except KeyError:
            raise ParseError("email must be provided")
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:

        fields = ["password"]

    def validate(self, data: Any) -> Any:

        password = data.get("password")
        token = self.context.get("kwargs").get("token")  # type: ignore
        encoded_pk = self.context.get("kwargs").get("encoded_pk")  # type: ignore

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data
