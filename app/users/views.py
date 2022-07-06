from app.users.models import UserFollowing
from app.users.serializers import FollowingSerializer, FollowersSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFollowingView(APIView):

    serializer_class = FollowingSerializer
    queryset = UserFollowing.objects.all()

class UserFollowerView(APIView):

    serializer_class = FollowersSerializer
    queryset = UserFollowing.objects.all()
