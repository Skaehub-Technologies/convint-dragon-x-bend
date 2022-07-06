from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import serializers
from app.users.models import UserFollowing
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    

    class Meta:
        model = User
        fields = (
            "id",
            "email",
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
        fields = ("id", "following_user_id", "created_at")

class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ("id", "user_id", "created_at")