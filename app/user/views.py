from typing import Any

from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CheckFollowingSerializer, UserFollowingSerializer

User = get_user_model()


class UserFollowView(APIView):
    def get_object(self, pk: Any) -> Any:
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request: Any, pk: Any, format: Any = None) -> Any:
        user = self.get_object(pk)
        serializer = UserFollowingSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Any, pk: Any, format: Any = None) -> Any:
        user = request.user
        follow = self.get_object(pk)
        serializer = CheckFollowingSerializer(
            data={"following": user.id, "follower": user.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_serializer = UserFollowingSerializer(follow)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def unfollow(self, request: Any, pk: Any, format: Any = None) -> Any:
        return Response(
            {"message": "you are no longer following him"},
            status=status.HTTP_200_OK,
        )
