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
from shop.serializers.apply import OwnListsSerializer
class ApplyView(APIView):

    # リストオーナー情報取得 GET
    def get(self, request, user_id):
        # リストオーナーを取得
        owner = get_object_or_404(User, pk=user_id)

        # 取得したオーナーに紐づくリストを取得
        lists = List.objects.filter(owner_id=user_id)
        serializer = OwnListsSerializer(lists, many=True)

        response_data = {
            'user_id': user_id,
            'user_name': owner.user_name,
            'user_icon': owner.user_icon,
            'lists': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    # 申請送信 POST
    def post(self, request, user_id=None):
        list_id = request.data.get('list_id')
        user_id = request.data.get('user_id')
        authority = request.data.get('authority')
        # リスト、ゲスト、オーナーを取得
        list_instance = get_object_or_404(List, pk=list_id)
        guest = get_object_or_404(User, pk=user_id)
        owner = get_object_or_404(User, pk=list_instance.owner_id)
        # 既存のMemberをチェック
        if Member.objects.filter(list_id=list_instance, guest_id=guest).exists():
            return Response({'detail': 'あなたはこのリストにすでに参加済み、または招待・申請中です'}, status=status.HTTP_400_BAD_REQUEST)
        #Memberテーブルにデータ保存
        new_guest = Member(list_id=list_instance, guest_id=guest, authority=authority, member_status = 2)        
        new_guest.save()
        # オーナーのrequestをTrueにする処理
        owner.request = True
        owner.save()
        
        member_status = 2

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