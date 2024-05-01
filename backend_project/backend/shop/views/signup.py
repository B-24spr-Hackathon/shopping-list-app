from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from shop.serializers.signup import SignupSerializer


"""
SignupView
ユーザー登録処理のView
"""
class SignupView(APIView):
    authentication_classes = []
    # POSTリクエストの処理
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = AccessToken.for_user(user)
            return Response({
                "user": serializer.data,
                "access": str(token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
