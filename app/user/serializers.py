from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import FollowUnfollow, Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class FollowUnfollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUnfollow
        fields = '__all__'


class FollowUnfollowSerializerSorted(serializers.ModelSerializer):
    class Meta:
        model = FollowUnfollow
        fields = ("user_id", "profile")