from rest_framework.views import APIView
from rest_framework.response import Response
from app.user.serializers import (
    UserSerializer,
    UserTokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token


class UserRegister(APIView):
    def post(self, request, format="json"):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json["token"] = token.key
                return Response(json)

        return Response(serializer.errors)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
