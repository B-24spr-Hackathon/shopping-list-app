from django.shortcuts import get_object_or_404
from rest_framework import status
from ..models import Item, List
from ..serializers.items import ItemSerializer, ItemCreateSerializer, ItemResponseSerializer, ItemUpdateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from shop.permissions import IsOwnerOrInviteeWithAuthority

class ItemCreateView(APIView):
    # JWT認証を要求、オーナーまたは編集権限を持つ招待者のみ許可
    permission_classes = [IsAuthenticated, IsOwnerOrInviteeWithAuthority]

    # アイテムリスト表示
    def get(self, request, list_id):      
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # 取得したリストに紐づくアイテムを取得
        items = Item.objects.filter(list_id=list_id)
        serializer = ItemSerializer(items, many=True)
        # レスポンスをカスタマイズ
        response_data = {
            'list_id': list_id,
            'list_name': list_instance.list_name,
            'items': serializer.data
        }
        return Response(response_data)

    
    # アイテム新規作成
    def post(self, request, list_id):
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        serializer = ItemCreateSerializer(data=request.data)
        # list_idを使ってListインスタンスを取得し、アイテムを保存
        if serializer.is_valid():
            serializer.save(list_id=list_instance)
        # 作成、保存されたアイテムをシリアライズして返す
            response_serializer = ItemResponseSerializer(serializer.instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailView(APIView):
    # JWT認証を要求、オーナーまたは編集権限を持つ招待者のみ許可
    permission_classes = [IsAuthenticated, IsOwnerOrInviteeWithAuthority]

        # アイテム更新            
    def patch(self, request, list_id, item_id):
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)

        # アイテムのインスタンスを取得
        item_instance = get_object_or_404(Item, pk=item_id)

        serializer = ItemUpdateSerializer(item_instance, data=request.data, context={"request": request}, partial=True)
    
        if serializer.is_valid():
            # データを更新して保存
            serializer.save()
            # 更新されたフィールドのみ辞書として取得
            update_fields = {field: request.data[field] for field in request.data}
            # 更新されたフィールドのみをレスポンスとして返す
            return Response(update_fields, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # アイテム削除
    def delete(self, request, list_id, item_id):
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # アイテムのインスタンスを取得
        item_instance = get_object_or_404(Item, pk=item_id)

        response_serializer = ItemResponseSerializer(item_instance)
        serialized_data = response_serializer.data

        item_instance.delete()
        # 削除したアイテムのデータを表示する
        return Response(serialized_data, status=status.HTTP_200_OK)



