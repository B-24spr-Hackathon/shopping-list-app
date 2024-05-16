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
from django.db.models import Q

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
        
        # ゲスト、リストを取得
        guest = get_object_or_404(Member, pk=member_id)
        list_instance = guest.list_id
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # ユーザー名を取得
        user_name = guest.guest_id.user_name
        # ゲストを削除
        guest.delete()

        # 削除されたゲストが他のリストに登録されているか確認
        owner_lists_count = List.objects.filter(owner_id=guest.guest_id).count()
        guest_lists_count = Member.objects.filter(guest_id=guest.guest_id, member_status=0).count()

        other_lists_count = owner_lists_count + guest_lists_count
        # have_listを更新
        if other_lists_count == 0:
            guest.guest_id.have_list = False

        guest.guest_id.save()

        # レスポンス用データ
        data = {
            'user_name': user_name,
        }
        return Response(data, status=status.HTTP_200_OK)
    
class EntryAcceptView(APIView):
    # JWT認証を要求
    permission_classes = [IsAuthenticated] 
        # 招待 承認機能 PATCH
    def patch(self, request, member_id):
        # ゲスト、リストを取得
        guest = get_object_or_404(Member, pk=member_id)
        list_instance = guest.list_id
        # member_statusカラムの値を更新
        guest.member_status = 0
        guest.save()
         # have_listをTrueに更新
        guest.guest_id.have_list = True
        guest.guest_id.save()

        data ={
            'member_status': guest.member_status,
        }
        return Response(data, status=status.HTTP_200_OK)