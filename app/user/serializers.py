from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.user.models import UserFollowing

User = get_user_model()


class CheckFollowingSerializer(serializers.Serializer):
    class Meta:
        model = UserFollowing
        fields = ("id", "following", "followers")

    def validate(self, data: Any) -> Any:

        followed = data.get("following")
        follower = data.get("followers")

        if followed is None or follower is None:
            raise serializers.ValidationError("Follow users.")
        else:
            if followed == follower:
                raise serializers.ValidationError(
                    {"detail": "You cannot follow this user."}
                )
        return data


class UserFollowingSerializer(serializers.ModelSerializer):

    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "following",
            "followers",
        )

    def get_following(self, obj: Any) -> Any:
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj: Any) -> Any:
        return FollowersSerializer(obj.followers.all(), many=True).data


class FollowingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="follower.username")

    class Meta:
        model = UserFollowing
        fields = ("username", "created_at")


class FollowersSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="following.username")

    class Meta:
        model = UserFollowing
        fields = ("username", "created_at")
