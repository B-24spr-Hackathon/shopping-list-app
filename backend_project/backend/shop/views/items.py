from django.shortcuts import get_object_or_404
from rest_framework import status
from ..models import Item, List
from ..serializers.items import ItemSerializer, ItemCreateSerializer, ItemResponseSerializer, ItemUpdateSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

class ItemView(APIView):
    # JWT認証を要求する
    permission_classes = [IsAuthenticated]

    # アイテムリスト表示
    def get(self, request, list_id):
        # owner または invitee, かつ list_idでアイテムをフィルタリング
        filters = (Q(list_id__owner_id=request.user) | Q(list_id__members__invitee_id=request.user)) & Q(list_id=list_id)
        items = Item.objects.filter(filters)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    # アイテム新規作成
    def post(self, request, list_id):
        # リストのオーナーまたはauthority=Trueのinviteeだけの条件でリストを取得
        list_instance = get_object_or_404(
            List.objects.filter(
                Q(pk=list_id),
                Q(owner_id=request.user) | Q(members__invitee_id=request.user, members__authority=True)
            )
        )
        serializer = ItemCreateSerializer(data=request.data)
        # list_idを使ってListインスタンスを取得し、アイテムを保存
        if serializer.is_valid():
            serializer.save(list_id=list_instance)
        # 作成、保存されたアイテムをシリアライズして返す
            response_serializer = ItemResponseSerializer(serializer.instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # アイテム更新            
    def patch(self, request, *args, **kwargs):
        user_id = request.user.id
        item_id = kwargs.get('item_id')        
        # owner または inviteeか、アイテムが存在するかフィルタリング
        filters = (Q(list_id__owner_id=user_id) | Q(list_id__members__invitee_id=user_id)) & Q(id=item_id)
        # アイテムを取得
        item = get_object_or_404(Item.objects.filter(filters))

        serializer = ItemUpdateSerializer(item, data=request.data, context={"request": request}, partial=True)
    
        if serializer.is_valid():
            saved_item = serializer.save()
            update_serializer = ItemResponseSerializer(saved_item)
            return Response(update_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
     # アイテム削除
    def delete(self, request, user_id, item_id):
        filters = (Q(list_id__owner_id=user_id) | Q(list_id__members__invitee_id=user_id)) & Q(id=item_id)
        # 削除するアイテムのインスタンスを取得
        item = get_object_or_404(Item.objects.filter(filters))
        # 削除する前にシリアライズしたデータを保存
        response_serializer = ItemResponseSerializer(item)
        serialized_data = response_serializer.data

        item.delete()
        # 削除したアイテムのデータを表示する
        return Response(serialized_data, status=status.HTTP_200_OK)   