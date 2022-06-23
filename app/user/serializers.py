from typing import Any

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.user.models import Profile, UserFollowing
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

    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "following",
            "followers",)

    # def validate(self, data):

    #     if data['password'] != data['confirm_password']:
    #         raise serializers.ValidationError("Passwords do not match")
    #     return data

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
        profile_instance = Profile.objects.create(user=user)  # noqa F841
        self.send_email(user)

        return user

    def get_following(self, obj):
        return UserFollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return FollowersSerializer(obj.followers.all(), many=True).data

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    bio = serializers.CharField(allow_blank=True, required=False)
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ("username", "bio")
        read_only_fields = ["username"]

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user_instance = User.objects.create(**user_data)
    #     profile_instance = Profile.objects.create(user=user_instance, **validated_data)
    #     return profile_instance


class UserFollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "following_user_id", "created")

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ("id", "user_id", "created")
