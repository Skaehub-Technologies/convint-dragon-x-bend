from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.user.token import account_activation_token
from app.user.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)
from speaksfer.settings.base import EMAIL_USER

from .models import Profile, UserFollowing

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
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
        fields = ("id", "email", "username", "password")

    @staticmethod
    def send_email(user: Any, request: Any) -> None:

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
        Profile.objects.create(user=user)
        self.send_email(user, request)

        return user


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
            return data

        raise serializers.ValidationError(
            "Invalid or expired token", code="invalid_token"
        )

    def save(self, **kwargs: Any) -> Any:
        user_id = force_str(
            urlsafe_base64_decode(self.validated_data.get("uidb64"))
        )
        user = User.objects.get(pk=user_id)
        user.is_verified = True
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username: Any = serializers.CharField(
        read_only=True, source="user.username"
    )
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Profile
        fields = ("username", "bio", "image")

    def update(self, instance: Any, validated_data: Any) -> Any:
        instance.bio = validated_data.get("bio", instance.bio)
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return


class UserFollowingSerializer(serializers.ModelSerializer):
    follow = serializers.SlugRelatedField(
        write_only=True, slug_field="id", queryset=User.objects.all()
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFollowing
        fields = ["id", "follow", "user", "following", "followers"]
        read_only_fields = ["id", "user", "following", "followers"]

    def validate(self, data: Any) -> Any:

        check_follow = UserFollowing.objects.filter(
            follower=data.get("user"), followed=data.get("follow")
        ).exists()
        if not check_follow:
            return data
        else:
            raise serializers.ValidationError(
                "You already following this user"
            )

    def create(self, validated_data: Any) -> Any:
        connection = UserFollowing.objects.create(
            follower=validated_data.get("user"),
            followed=validated_data.get("follow"),
        )

        return connection


class FollowersFollowingSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("following", "followers")

    def get_following(self, obj: Any) -> Any:

        return FollowedSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj: Any) -> Any:

        return FollowerSerializer(obj.followers.all(), many=True).data


class FollowedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source="followed.id")
    username = serializers.ReadOnlyField(source="followed.username")

    class Meta:
        model = UserFollowing
        fields = ["id", "username", "created_at"]


class FollowerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source="follower.id")
    username = serializers.ReadOnlyField(source="follower.username")

    class Meta:
        model = UserFollowing
        fields = ["id", "username", "created_at"]
