from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from shop.serializers.login import LoginSerializer, LoginResponseSerializer
import logging

logger = logging.getLogger("backend")


"""
LoginView
ログイン処理のView
"""
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    # POSTリクエストの処理
    def post(self, request):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        logger.info(f"{request.data}")

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token = AccessToken.for_user(user)
            response_serializer = LoginResponseSerializer(user)
            return Response({
                "user": response_serializer.data,
                "access": str(token)
            }, status=status.HTTP_200_OK)

        logger.error(f"{serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
