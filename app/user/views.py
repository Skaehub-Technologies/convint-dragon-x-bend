from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from typing import Any
from .serializers import UserFollowingSerializer, CheckUserFollowingSerializer

User = get_user_model()

class UserFollow(generics.GenericAPIView):

    def get(self, request: Any, pk: Any, format: Any = None) -> Any:
        user = self.get_object(pk)
        serializer = UserFollowingSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Any, pk: Any, format: Any = None) -> Any:
        user = request.user
        follow = self.get_object(pk)
        serializer = CheckUserFollowingSerializer(
            data={"following": user.id, "follower": follow.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer_two = UserFollowingSerializer(follow)
        return Response(serializer_two.data, status=status.HTTP_200_OK)    

   