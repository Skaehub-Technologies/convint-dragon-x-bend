from rest_framework.views import APIView
from rest_framework.response import Response
from app.user.serializers import (
    User,
    UserSerializer,
    UserTokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
