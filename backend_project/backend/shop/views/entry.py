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
        # ゲスト、リストを取得
        guest = get_object_or_404(Member, pk=member_id)
        list_instance = guest.list_id
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # authorityカラムの値を更新
        new_authority = request.data.get('authority')
        if new_authority is not None:
            guest.authority = new_authority
            guest.save()

        data ={
            'authority': guest.authority,
        }
        return Response(data, status=status.HTTP_200_OK)

    # 招待・申請機能　共有解除 DELETE
    def delete(self, request, member_id):
        # ゲストを取得
        guest = get_object_or_404(Member, pk=member_id)
        guest_user_name = guest.guest_id.user_name
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, guest) 

        guest.delete()

        return Response(guest, status=status.HTTP_200_OK)
