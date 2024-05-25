from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import List, Member, User
from shop.authentication import CustomJWTAuthentication
from django.shortcuts import get_object_or_404
from shop.permissions import IsOwner
from rest_framework.response import Response
from django.db.models import Q
import logging

logger = logging.getLogger('backend')

class EntryView(APIView):
    # JWT認証を要求、オーナーのみ許可
    permission_classes = [IsAuthenticated, IsOwner] 

    # 招待・申請機能  編集権限変更 PATCH
    def patch(self, request, member_id):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        logger.info(f"{request.data}")

        # ゲスト、リストを取得
        try:
            guest = get_object_or_404(Member, pk=member_id)
            list_instance = guest.list_id
        except Http404:
            logger.error("メンバーが存在しない")
            return Response({"error": "メンバーが存在しません"},
                            status=status.HTTP_404_NOT_FOUND)
        

        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # authorityカラムの値を更新
        new_authority = request.data.get('authority')
        if new_authority is not None:
            guest.authority = new_authority
            guest.save()
            logger.info(f'ゲストの編集権限を更新: {guest.authority}')

        data ={
            'authority': guest.authority,
        }
        return Response(data, status=status.HTTP_200_OK)        



    # 招待・申請機能　共有解除 DELETE
    def delete(self, request, member_id):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        if request.data:
            logger.error(f"{request.data}")

        try:
            # ゲスト、リストを取得
            guest = get_object_or_404(Member, pk=member_id)
            list_instance = guest.list_id
        except Http404:
            logger.error("メンバーが存在しない")
            return Response({"error": "メンバーが存在しません"},
                            status=status.HTTP_404_NOT_FOUND) 

        # member_status=0以外の場合、このメソッドでは処理できない
        if guest.member_status != 0:
            logger.error('招待・申請中のゲストの削除はできない')
            return Response({'error': '招待・申請中のゲストの削除はここからはできません'}, status=status.HTTP_400_BAD_REQUEST)
               
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # ユーザー名を取得
        user_name = guest.guest_id.user_name
        # ゲストを削除
        guest.delete()
        logger.info(f'ゲスト削除: {guest}')

        # 削除されたゲストが他のリストに登録されているか確認
        owner_lists_count = List.objects.filter(owner_id=guest.guest_id).count()
        guest_lists_count = Member.objects.filter(guest_id=guest.guest_id, member_status=0).count()

        other_lists_count = owner_lists_count + guest_lists_count
        # have_listを更新
        if other_lists_count == 0:
            guest.guest_id.have_list = False

        guest.guest_id.save()
        logger.info(f'ゲストのhave_list更新: {guest.guest_id.have_list}')

        # レスポンス用データ
        data = {
            'user_name': user_name,
        }
        return Response(data, status=status.HTTP_200_OK)



# 招待 申請承認機能　
class EntryAcceptView(APIView):
           
    # 承認処理    
    def patch(self, request, member_id):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        logger.info(f"{request.data}")
        try:
            # ゲスト、リスト、アクセスしているユーザーを取得
            guest = get_object_or_404(Member, pk=member_id)
            list_instance = guest.list_id
            current_user: User = request.user
        except Http404:
            logger.error("ゲストが存在しない")
            return Response({"error": "ゲストが存在しません"},
                            status=status.HTTP_404_NOT_FOUND)    

        # リストのオーナーでもゲストでもない場合は403 Forbiddenを返す
        if current_user != list_instance.owner_id and current_user != guest.guest_id:            
            logger.error('承認権限なし')
            return Response({'error': '承認する権限がありません'}, status=status.HTTP_403_FORBIDDEN)
        
        # リストのオーナーは、所有するリストのmember_status=2のデータのみ承認可能
        if current_user == list_instance.owner_id:
            # オーナーが他のリストの申請を承認しようとした場合
            if guest.list_id != list_instance:
                logger.error('他のリストの申請を承認しようとしています')
                return Response({'error': '他のリストの申請を承認できません'}, status=status.HTTP_403_FORBIDDEN)
            if guest.member_status != 2:
                logger.error('オーナーは申請しか承認できない')
                return Response({'error': '自身が招待したものは自身で承認できません'}, status=status.HTTP_403_FORBIDDEN)

        # リストのユーザー（ゲスト）は、自分が招待されている member_status=1 のデータのみ承認可能
        if current_user == guest.guest_id:
            # 自分以外のメンバーを承認しようとする場合
            if guest.guest_id != current_user:
                logger.error('ゲストは他のメンバーのステータスを承認できない')
                return Response({'error': '他のメンバーのステータスを承認できません'}, status=status.HTTP_403_FORBIDDEN)
            # member_status が 1 以外のものを承認しようとする場合
            if guest.member_status != 1:
                logger.error('ゲストは招待しか承認できない')
                return Response({'error': '自身が申請したものは自身で承認できません'}, status=status.HTTP_403_FORBIDDEN)

        # member_statusカラムの値を更新
        guest.member_status = 0
        guest.save()
        logger.info(f'承認完了member_statusを更新: {guest.member_status}')

        # ゲストのhave_listがFalseだった場合Trueに更新
        if not guest.guest_id.have_list:
            guest.guest_id.have_list = True
            guest.guest_id.save()
            logger.info(f'ゲストのhave_listを更新: {guest.guest_id.have_list}')

        # アクセスユーザーがゲストの場合
        if current_user == guest.guest_id:
            # 他に招待中のステータスがなければ招待フラグをFalseに
            other_invites = Member.objects.filter(guest_id=guest.guest_id, member_status=1).exists()
            if not other_invites:
                guest.guest_id.invitation = False
                guest.guest_id.save()
                logger.info(f'ゲストの招待フラグを更新: {guest.guest_id.invitation}')
        # アクセスユーザーがリストオーナーの場合
        elif current_user == list_instance.owner_id:
            # 他に申請中のステータスがなければ申請フラグをFalseに
            owner_lists = List.objects.filter(owner_id=current_user)
            other_requests = Member.objects.filter(list_id__in=owner_lists, member_status=2).exists()
            if not other_requests:
                list_instance.owner_id.request = False
                list_instance.owner_id.save()
                logger.info(f'オーナーのリクエストフラグを更新: {list_instance.owner_id.request}')
        
        data ={'member_status': guest.member_status,}
        return Response(data, status=status.HTTP_200_OK)

    
# 招待 申請 拒否・中止機能　DELETE
class EntryDeclineView(APIView):

    def delete(self, request, member_id):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        if request.data:
            logger.error(f"{request.data}")

        try:
            # ゲスト、リスト、アクセスしているユーザーを取得
            guest = get_object_or_404(Member, pk=member_id)
            list_instance = guest.list_id
            current_user: User = request.user

        except Http404:
            logger.error("ゲストが存在しない")
            return Response({"error": "ゲストが存在しません"},
                            status=status.HTTP_404_NOT_FOUND)
        # リストのオーナーでもゲストでもない場合は403 Forbiddenを返す
        if current_user != list_instance.owner_id and current_user != guest.guest_id:
            logger.error('拒否・中止権限なし')
            return Response({'error': '拒否または中止する権限がありません'}, status=status.HTTP_403_FORBIDDEN)
        
        # member_statusを取得
        member_status = guest.member_status
        # ゲストを取得
        guest_user = guest.guest_id
        # オーナを取得
        owner_user = list_instance.owner_id
        # ゲストのユーザー名を取得
        user_name = guest.guest_id.user_name

        # member_status=0の場合、このメソッドでは処理できない
        if guest.member_status == 0:
            logger.error('参加済みのゲストは拒否・中止できない')
            return Response({'error': '参加済みのゲストの削除はここからはできません'}, status=status.HTTP_400_BAD_REQUEST)
        
        # member_status=1の場合,ゲストがアクセス時は招待拒否、オーナーがアクセス時は招待中止
        if member_status == 1:              
            # ゲストについて他に招待中のステータスがなければinvitationをFalseに
            other_invites = Member.objects.filter(guest_id=guest_user, member_status=1).exclude(pk=member_id).exists()
            if not other_invites:
                guest_user.invitation = False
                guest_user.save()
                logger.info(f'ゲストの招待フラグ更新: {guest_user.invitation}')
        # member_status=2の場合、ゲストがアクセス時は申請中止、オーナーがアクセス時は申請拒否
        elif member_status == 2:
            # オーナーについて他に申請中のステータスがなければrequestをFalseに
            owner_lists = List.objects.filter(owner_id=current_user)
            other_requests = Member.objects.filter(list_id__in=owner_lists, member_status=2).exclude(pk=member_id).exists()
            if not other_requests:
                owner_user.request = False
                owner_user.save()
                logger.info(f'オーナーのリクエストフラグ更新: {owner_user.request}')

                # 招待・申請を拒否・中止
        guest.delete()
        logger.info(f'拒否・中止完了: {guest}')

        # レスポンス用データ
        data = {
            'user_name': user_name,
        }
        return Response(data, status=status.HTTP_200_OK) 
    
  
# 招待・申請一覧を表示 GET
class EntryStatusView(APIView):

    def get(self, request):
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        if request.data:
            logger.error(f"{request.data}")
   
        user = request.user

        # アクセスユーザーが所有するリストのIDを取得
        owned_list_ids = List.objects.filter(owner_id=user).values_list('list_id', flat=True)
        # ユーザーが関連するすべてのMembersレコードを取得
        all_members = Member.objects.filter(Q(guest_id=user) | Q(list_id__in=owned_list_ids))
        
        member_data = []

        for member  in all_members:
            is_owner = member.list_id.list_id in owned_list_ids
            member_data.append({
                'member_id': member.member_id,
                'guest_name': member.guest_id.user_name,
                'member_status': member.member_status,
                'list_id': member.list_id.list_id,
                'list_name': member.list_id.list_name,
                'owner_name': member.list_id.owner_id.user_name,
                'is_owner': is_owner,
            })
        return Response(member_data, status=status.HTTP_200_OK)
