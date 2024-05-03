from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from shop.models import List
from shop.authentication import CustomJWTAuthentication
from shop.serializers.user import SignupSerializer, GetUpdateUserSerializer


"""
UserView
ユーザーに関する処理（CRUD）のView
"""
class UserView(APIView):
    # リクエストメソッドごとに認証クラスを設定
    def get_authenticators(self):
        if self.request.method == "POST":
            return []
        else:
            return [CustomJWTAuthentication()]

    # リクエストメソッドごとにパーミッションクラスを設定
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        else:
            return  [IsAuthenticated()]


    # GETリクエストの処理（表示）
    def get(self, request):
        user = request.user
        response_serializer = GetUpdateUserSerializer(user)
        lists = List.objects.filter(owner_id=user.user_id).values("list_id", "list_name")
        response_lists = [{"list_id": i["list_id"], "list_name": i["list_name"]} for i in lists]
        return Response({
            "user": response_serializer.data,
            "lists": response_lists
        }, status=status.HTTP_200_OK)


    # POSTリクエストの処理（登録）
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


    # PATCHリクエストの処理（更新）
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = GetUpdateUserSerializer(user, data=request.data,
                                       context={"request": request},
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    # DELETEリクエストの処理（退会）
    def delete(self, request):
        user = request.user
        response_user = {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email,
            "user_icon": user.user_icon
        }
        user.delete()
        return Response(response_user, status=status.HTTP_200_OK)
