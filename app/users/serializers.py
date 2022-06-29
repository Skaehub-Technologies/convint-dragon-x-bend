from typing import Any
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from speaksfer.settings.base import EMAIL_USER
from app.users.models import Profile

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

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("username", "bio", "image")
        read_only_fields = "username"

class EmailSerializer(serializers.Serializer):
   
    email = serializers.EmailField()

    class Meta:
        fields = ("email",)


class ResetPasswordSerializer(serializers.Serializer):
   
    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:
        field = ("password")

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.get(pk=pk)
        user = User.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data