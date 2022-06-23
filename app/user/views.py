from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from app.user.models import Profile, UserFollowing
from app.user.serializers import ProfileSerializer, UserSerializer, UserFollowingSerializer
from rest_framework import viewsets

User = get_user_model()



class UserRegister(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class UserProfile(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer_profile = ProfileSerializer(data=request.data)
        serializer_profile.is_valid(raise_exception=True)
        user_profile = serializer_profile.save()
        return Response(user_profile)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    lookup_field = "user"
    queryset = Profile.objects.all()


class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserFollowingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly)
    lookup_field = "following"
    serializer_class = UserFollowingSerializer

    def get_queryset(self):
        return self.request.user.UserFollowing.all()
