from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from shop.serializers.login import LoginSerializer, LoginResponseSerializer


"""
LoginView
ログイン処理のView
"""
class LoginView(APIView):
    authentication_classes = []
    
    # POSTリクエストの処理
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token = AccessToken.for_user(user)
            response_serializer = LoginResponseSerializer(user)
            return Response({
                "user": response_serializer.data,
                "access": str(token)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
