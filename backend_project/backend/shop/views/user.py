from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from shop.models import List, Member
from shop.authentication import CustomJWTAuthentication
from shop.serializers.user import SignupSerializer, GetUpdateUserSerializer
import logging

logger = logging.getLogger("backend")


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
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        if request.data:
            logger.error(f"{request.data}")

        user = request.user
        response_serializer = GetUpdateUserSerializer(
            user, context={"request": request}
        )

        # user_idより所有するリストのlist_id, list_nameを取得
        lists = List.objects.filter(owner_id=user.user_id).values("list_id", "list_name")
        response_lists = [{
            "list_id": i["list_id"],
            "list_name": i["list_name"],
            "is_owner": True,
            "authority": True
            } for i in lists]

        # ゲストになっているリストを取得
        members = Member.objects.filter(guest_id=user, member_status=0)
        response_members = [{
            "list_id": j.list_id.list_id,
            "list_name": j.list_id.list_name,
            "is_owner": False,
            "authority": j.authority
            } for j in members]

        # レスポンスデータを作成
        response = response_lists + response_members

        return Response({
            "user": response_serializer.data,
            "lists": response
        }, status=status.HTTP_200_OK)

    # POSTリクエストの処理（登録）
    def post(self, request):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        logger.info(f"{request.data}")

        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = AccessToken.for_user(user)
            return Response({
                "user": serializer.data,
                "access": str(token)
            }, status=status.HTTP_201_CREATED)

        logger.error(f"{serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCHリクエストの処理（更新）
    def patch(self, request, *args, **kwargs):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        logger.info(f"{request.data}")

        # line_idの更新リクエストの場合はエラーを返す
        if request.data.get("line_id"):
            logger.error("line_idの更新リクエスト")
            return Response({"error": "line_idの更新はできません"},
                            status=status.HTTP_400_BAD_REQUEST)
        # user_idの更新リクエストの場合はエラーを返す
        elif request.data.get("user_id"):
            logger.error("user_idの更新リクエスト")
            return Response({"error": "user_idの更新はできません"},
                            status=status.HTTP_400_BAD_REQUEST)
        # line_statusの更新リクエストの場合はエラーを返す
        elif request.data.get("line_status") is not None:
            logger.error("user_idの更新リクエスト")
            return Response({"error": "line_statusの更新はできません"},
                            status=status.HTTP_400_BAD_REQUEST)
        # have_listの更新リクエストの場合はエラーを返す
        elif request.data.get("have_list") is not None:
            logger.error("have_listの更新リクエスト")
            return Response({"error": "have_listの更新はできません"},
                            status=status.HTTP_400_BAD_REQUEST)
        # remindをTrueにするリクエストでline_statusがFalseの場合はエラーを返す
        elif request.data.get("remind") and not request.user.line_status:
            logger.error("友達追加していないユーザーの通知ONリクエスト")
            return Response({"error": "友達追加が必要です"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        serializer = GetUpdateUserSerializer(user, data=request.data,
                                             context={"request": request},
                                             partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "user": serializer.data
            }, status=status.HTTP_200_OK)

        logger.error(f"{serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETEリクエストの処理（退会）
    def delete(self, request):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        if request.data:
            logger.error(f"{request.data}")

        user = request.user
        response_user = {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email,
            "user_icon": user.user_icon
        }
        user.delete()
        return Response(response_user, status=status.HTTP_200_OK)
