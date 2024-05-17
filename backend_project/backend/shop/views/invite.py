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
        logger.info('InviteView GET method called')
        try:
            # 招待者を取得
            guest = get_object_or_404(User, pk=user_id)
            logger.debug(f'Guest user retrieved: {guest}')
            # パーミッションチェックを実行
            self.check_object_permissions(self.request,guest)
            guest_data = FindUserSerializer(guest).data
            logger.info(f'Guest data serialized: {guest_data}')

            return Response(guest_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f'Error in GET method: {str(e)}')
            return Response({'detail': 'Error retrieving guest data'}, status=status.HTTP_400_BAD_REQUEST)


    # 招待処理　招待送信　POST
    def post(self, request, user_id=None):
        logger.info('InviteView POST method called')
        try:
            list_id = request.data.get('list_id')
            user_id = request.data.get('user_id')
            authority = request.data.get('authority')
            logger.debug(f'Received data - list_id: {list_id}, user_id: {user_id}, authority: {authority}')
            # リストとゲストを取得
            list_instance = get_object_or_404(List, pk=list_id)
            logger.debug(f'List instance retrieved: {list_instance}')
            guest = get_object_or_404(User, pk=user_id)
            logger.debug(f'Guest user retrieved: {guest}')
            # パーミッションチェックを実行
            self.check_object_permissions(self.request, list_instance)
            # 既存のMemberをチェック
            if Member.objects.filter(list_id=list_instance, guest_id=guest).exists():
                logger.warning('Guest already part of the list or invited/requested')
                return Response({'detail': 'このゲストはこのリストにすでに参加済み、または招待・申請中です'}, status=status.HTTP_400_BAD_REQUEST)
            #Memberテーブルにデータ保存
            new_guest = Member(list_id=list_instance, guest_id=guest, authority=authority, member_status = 1)        
            new_guest.save()
            logger.info(f'New guest member created: {new_guest}')

            # ゲストのinvitationをTrueにする処理
            guest.invitation = True
            guest.save()
            logger.info(f'Guest invitation updated for user: {guest.user_name}')
            
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
            logger.info(f'Response data created: {data}')
            return Response(data, status=status.HTTP_201_CREATED) 
        
        except Exception as e:
            logger.error(f'Error in POST method: {str(e)}')
            return Response({'detail': 'Error inviting guest'}, status=status.HTTP_400_BAD_REQUEST)