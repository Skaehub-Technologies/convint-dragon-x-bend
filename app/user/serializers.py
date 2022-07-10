from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.user.models import UserFollowing
from django.utils.http import urlsafe_base64_decode
from rest_framework.authtoken.models import Token

User = get_user_model()

class CheckUserFollowingSerializer(serializers.Serializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "following", "follower")

    def validate(self, data: Any) -> Any:
        
        following = data.get("following")
        follower = data.get("follower")
        url_kwargs = self.context.get("kwargs")
        encoded_pk = url_kwargs.get("encoded_pk")  # type: ignore[union-attr]

        if following is None or follower is None:
            raise serializers.ValidationError("Must follow a user.")
        pk = urlsafe_base64_decode(encoded_pk).decode()

        user = User.objects.get(pk=pk)
        if following == follower:
            raise serializers.ValidationError(
                {"detail": "You cannot follow this user."}
            )
        user.save()
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

    def get_following(self, obj: Any)-> Any:
        return FollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj: Any)-> Any:
        return FollowersSerializer(obj.followers.all(), many=True).data

    def create(self, validated_data: Any)-> Any:
        user = User.objects.create_user(**validated_data)  
        Token.objects.create(user=user) 
        return user    

class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "following", "username", "created_at")

class FollowersSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "follower", "username", "created_at")