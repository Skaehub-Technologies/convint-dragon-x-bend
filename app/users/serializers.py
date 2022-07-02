from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from typing import Any
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.request import Request
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

class EmailSerializer(serializers.Serializer):

    email = serializers.EmailField()

    class Meta:
        abstract = True
        fields = "email"


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset Password Serializer.

    """

    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:
        field = "password"


    @staticmethod
    def send_email(user: Any, request: Request) -> None:

        current_site_info = get_current_site(request)
        email_body = render_to_string(
            "password_reset.html",
            {
                "user": user,
                "domain": current_site_info.domain,
                "encoded_pk" :urlsafe_base64_encode(force_bytes(user.pk)),
                "token" : PasswordResetTokenGenerator().make_token(user),
            
            },
        )

        send_mail(
            "Verify  your email!",
            email_body,
            EMAIL_USER,
            [user.email],
            fail_silently=False,
        )
    # @staticmethod
    # def send_email(
    #     request: Any, user: Any, encoded_pk: str, token: str
    # ) -> dict:
    #     current_site = get_current_site(request).domain
    #     relative_link = reverse(
    #         "reset-password",
    #         kwargs={"encoded_pk": encoded_pk, "token": token},
    #     )
    #     absurl = f"http://{current_site}{relative_link}"
    #     body = {"user": user, "link": absurl}
    #     data = {
    #         "subject": "PASSWORD RESET",
    #         "body": body,
    #         "recipient": user.email,
    #     }

    #     return data

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
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data


   