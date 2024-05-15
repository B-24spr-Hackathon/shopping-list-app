from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import List, Member, User
from shop.authentication import CustomJWTAuthentication
from shop.serializers.invite import FindUserSerializer
from django.shortcuts import get_object_or_404
from shop.permissions import IsOwner

class EntryView(APIView):
    # JWT認証を要求、オーナーのみ許可
    permission_classes = [IsAuthenticated, IsOwner] 

    # 招待・申請機能  編集権限変更 PATCH
    def patch(self, request, member_id):
        # ゲストを取得
        guest = get_object_or_404(Member, pk=member_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, guest)
        # authorityカラムの値を更新
        new_authority = 'new_authority_value'
        guest.authority = new_authority
        guest.save()
        # 更新後のデータを返す
        data = {
            'authority' : guest.authority,
        }
        return Response(data, status=status.HTTP_200_OK)

    # 招待・申請機能　共有解除 DELETE
    def delete(self, request, member_id):
        # ゲストを取得
        guest = get_object_or_404(Member, pk=member_id)
        guest_user_name = guest.guest_id.user_name
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, guest) 



    # リスト設定（削除）DELETE
    def delete(self, request, list_id):
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # 削除する前にシリアライズしたデータを保存
        response_serializer = ListResponseSerializer(list_instance)
        serialized_data = response_serializer.data

        list_instance.delete()

        return Response(serialized_data, status=status.HTTP_200_OK)