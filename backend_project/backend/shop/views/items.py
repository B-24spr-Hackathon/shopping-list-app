from django.shortcuts import get_object_or_404
from rest_framework import status
from ..models import Item, List
from ..serializers.items import ItemSerializer, ItemCreateSerializer, ItemResponseSerializer, ItemUpdateSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

class ItemCreateView(APIView):
    # JWT認証を要求する
    #permission_classes = [IsAuthenticated]

    # アイテムリスト表示
    def get(self, request, list_id):      
        # リストのオーナーまたはauthority=Trueのinviteeだけの条件でリストを取得
        list_instance = get_object_or_404(
            List.objects.filter(
                Q(pk=list_id),
                Q(owner_id=request.user) | Q(members__invitee_id=request.user, members__authority=True)
            )
        )
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

class ItemDetailView(APIView):
    # JWT認証を要求する
    #permission_classes = [IsAuthenticated]

        # アイテム更新            
    def patch(self, request, list_id, item_id):
        # アイテムのインスタンスを取得
        item_instance = get_object_or_404(Item, pk=item_id)
        # リストのオーナーまたは権限を持つ招待者かどうかをチェック
        list_instance = get_object_or_404(
            List.objects.filter(
                Q(pk=list_id),
                Q(owner_id=request.user) | Q(members__invitee_id=request.user, members__authority=True)
            )
        )

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
        # アイテムのインスタンスを取得
        item_instance = get_object_or_404(Item, pk=item_id)
        # リストのオーナーまたは権限を持つ招待者かどうかをチェック
        list_instance = get_object_or_404(
            List.objects.filter(
                Q(pk=list_id),
                Q(owner_id=request.user) | Q(members__invitee_id=request.user, members__authority=True)
            )
        )
        # 権限が確認できた後にアイテムを削除
        if list_instance:
            # 削除する前にシリアライズしたデータを保存
            response_serializer = ItemResponseSerializer(item_instance)
            serialized_data = response_serializer.data
            item_instance.delete()
            # 削除したアイテムのデータを表示する
            return Response(serialized_data, status=status.HTTP_200_OK)
        
        return Response({"detail": "削除する権限がありません"}, status=status.HTTP_403_FORBIDDEN)



