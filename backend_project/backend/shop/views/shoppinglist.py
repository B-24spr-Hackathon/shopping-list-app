from django.shortcuts import get_object_or_404
from rest_framework import status
from shop.models import Item, List
from shop.serializers.shoppinglist import ShoppingListSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


# 買い物リスト表示(GET)
class ShoppingListView(APIView):
    # JWT認証を要求する
    permission_classes = [IsAuthenticated]  

    def get(self, request, list_id):
        # リストのオーナーまたはinviteeの条件でリストを取得
        list_instance = get_object_or_404(
            List.objects.filter(
                Q(pk=list_id),
                Q(owner_id=request.user) | Q(members__invitee_id=request.user)
            )
        )
        # リストに紐づくアイテムを取得
        items = Item.objects.filter(list_id=list_id, to_list=True)
        serializer = ShoppingListSerializer(items, many=True)

        # authorityの値を取得(オーナーの場合は自動的にTrue)
        if list_instance.owner_id == request.user:
            authority = True
        else:
            member = Member.objects.filter(list_id=list_id, invitee_id=request.user).first()
            authority = member.authority
            #else:
                #authority = False

            

        #list_instance = List.objects.filter(filters)
        # リストが見つからない場合エラーを返す
        #f not lists.exists():
            #return Response({"message": "リストが見つからないか、アクセス権限がありません。"}, status=status.HTTP_404_NOT_FOUND)
        

        serializer = ShoppingListSerializer(list_instance)

        response_data = {
            'list_id': list_id,
            'list_name': list_instance.list_name,
            'authority': authority,
            'items': serializer.data

        }
        return Response(response_data)
    
