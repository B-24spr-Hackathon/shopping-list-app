from django.shortcuts import get_object_or_404
from rest_framework import status
from shop.models import Item, List, Member
from shop.serializers.shoppinglist import ShoppingListSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from shop.permissions import IsOwnerOrInvitee


# 買い物リスト表示(GET)
class ShoppingListView(APIView):
    # JWT認証を要求する
    permission_classes = [IsAuthenticated, IsOwnerOrInvitee] 

    def get(self, request, list_id):
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # オブジェクトレベルのパーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # リストに紐づくアイテムを取得
        items = Item.objects.filter(list_id=list_id, to_list=True)
        serializer = ShoppingListSerializer(items, many=True)
        # authorityの値を取得(オーナーの場合は自動的にTrue)
        if list_instance.owner_id == request.user:
            authority = True
        else:
            member = Member.objects.filter(list_id=list_id, invitee_id=request.user).first()
            authority = member.authority
      
        response_data = {
            'list_id': list_id,
            'list_name': list_instance.list_name,
            'authority': authority,
            'items': serializer.data
        }
        return Response(response_data)
    
