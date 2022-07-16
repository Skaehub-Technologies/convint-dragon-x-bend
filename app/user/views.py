from typing import Any

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FollowUnfollowSerializer, ProfileSerializer, FollowUnfollowSerializerSorted
from .models import Profile, FollowUnfollow


User = get_user_model()
class ProfileDetails(APIView):
    def get(self, request):
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response("Profile successfully created")


# This class is used for fetch individual profile by using id.
class ViewsProfile(APIView):
    def get(self, request, pk):
        profile = Profile.objects.get(id=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

# This class is used for follow a profile.
class FollowProfile(APIView):
    def post(self, request, user_pk, profile_pk):
        check_follow = FollowUnfollow.objects.filter(user_id=user_pk, profile=profile_pk, follow_status='follow')
        if not check_follow:
            serializer = FollowUnfollowSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response("Successfully followed")
        else:
            return Response("You are already followed the user")


# This class is used for unfollow a profile.
class UnFollowProfile(APIView):
    def post(self, request, user_pk, profile_pk):
        check_follow = FollowUnfollow.objects.filter(user_id=user_pk, profile=profile_pk, follow_status='follow')
        if check_follow:
            check_follow.delete()
            return Response("Successfully unfollowed")
        else:
            return Response("You haven't followed anyone yet")


# This class is used to find all followers of a profile.
class ViewFollowers(APIView):
    def get(self, request, pk):
        fetch_profile = FollowUnfollow.objects.filter(profile=pk, follow_status='follow')
        if fetch_profile:
            serializer = FollowUnfollowSerializerSorted(fetch_profile, many=True)
            return Response(serializer.data)
        else:
            return Response("You don't have followers")


# This class is used to find all followings of a user.
class ViewFollowings(APIView):
    def get(self, request, pk):
        fetch_user = User.objects.get(id=pk)
        following_user = fetch_user.followunfollow_set.all()
        serializer = FollowUnfollowSerializerSorted(following_user, many=True)
        return Response(serializer.data)