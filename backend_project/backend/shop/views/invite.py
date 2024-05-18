from django.http import Http404
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
import logging

logger = logging.getLogger('backend')

class InviteView(APIView):
    # JWT認証を要求、オーナーのみ許可
    permission_classes = [IsAuthenticated, IsOwner]
    # GETメソッドだけは誰でも可
    def get_permissions(self):
       if self.request.method == 'GET':
           return [IsAuthenticated()] 
       return [IsAuthenticated(), IsOwner()]
    
    # 招待処理　招待者情報取得 GET
    def get(self, request, user_id):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        if request.data:
            logger.error(f"{request.data}")

        try:
            # 招待者を取得
            guest = get_object_or_404(User, pk=user_id)
            # パーミッションチェックを実行
            self.check_object_permissions(self.request,guest)
            guest_data = FindUserSerializer(guest).data

            return Response(guest_data, status=status.HTTP_200_OK)
        
        except Http404:
            logger.error('ユーザーが存在しない')
            return Response({'error': 'ユーザーが存在しません'}, status=status.HTTP_404_NOT_FOUND)


    # 招待処理　招待送信　POST
    def post(self, request, user_id=None):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        logger.info(f"{request.data}")

        list_id = request.data.get('list_id')         
        user_id = request.data.get('user_id')        
        authority = request.data.get('authority')
        
        # リストとゲストを取得
        try: 
            list_instance = get_object_or_404(List, pk=list_id)
            guest = get_object_or_404(User, pk=user_id)
            owner = get_object_or_404(User, pk=list_instance.owner_id)

        except Http404 as e:
            if 'List' in str(e):
                logger.error("リストが存在しない")
                return Response({"error": "リストが存在しません"},
                            status=status.HTTP_404_NOT_FOUND)
            elif 'User' in str(e): 
                logger.error("ユーザーが存在しない")      
                return Response({"error": "ユーザーが存在しません"},
                            status=status.HTTP_404_NOT_FOUND) 
                
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # 既存のMemberをチェック
        if Member.objects.filter(list_id=list_instance, guest_id=guest).exists():
            logger.error("すでに参加済または招待・申請中")
            return Response({'error': 'このゲストはこのリストにすでに参加済み、または招待・申請中です'}, status=status.HTTP_400_BAD_REQUEST)
        # オーナーは自分を招待できない
        if guest == owner:
            logger.error("自分のリストには自分を招待できない")
            return Response({'error': 'オーナー自身を招待できません'}, status=status.HTTP_400_BAD_REQUEST)
        #Memberテーブルにデータ保存
        new_guest = Member(list_id=list_instance, guest_id=guest, authority=authority, member_status = 1)            
        new_guest.save()
        logger.info(f'新しいレコードを登録: {guest.user_id}')
        # ゲストのinvitationをTrueにする処理
        guest.invitation = True
        guest.save()
        logger.info(f'ゲストの招待フラグを更新: {guest.invitation}')
        
        member_status = 1
        
        # レスポンス用のデータ作成
        data = {
            'list_id': list_instance.list_id,
            'list_name': list_instance.list_name,
            'guest_id': user_id,
            'user_name': guest.user_name,
            'user_icon': guest.user_icon,
            'authority': authority,
            'member_status': member_status, 
        }
        return Response(data, status=status.HTTP_201_CREATED) 
   
