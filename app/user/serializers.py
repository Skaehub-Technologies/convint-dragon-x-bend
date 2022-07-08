from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from app.user.utils import create_reset_email, generate_reset_token, send_email

User = get_user_model()


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

    class Meta:
        fields = ["email"]

    def validate(self, attrs: Any) -> Any:

        request = self.context.get("request")
        email = attrs.get("email")
        user = generate_reset_token(email)

        if user:
            email_data = create_reset_email(request, *user)
            send_email("password_reset.html", email_data)
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6,
    )

    class Meta:

        fields = ["password"]

    def validate(self, data: Any) -> Any:

        password = data.get("password")
        url_kwargs = self.context.get("kwargs")
        token = url_kwargs.get("token")  # type: ignore[union-attr]
        encoded_pk = url_kwargs.get("encoded_pk")  # type: ignore[union-attr]

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError(
                {"detail": "The reset token is invalid"}
            )

        user.set_password(password)
        user.save()
        return data
