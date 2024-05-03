from django.shortcuts import get_object_or_404
from rest_framework import status
from ..models import Item, List
from ..serializers.items import ItemSerializer, ItemCreateSerializer, ItemResponseSerializer, ItemUpdateSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# アイテムリスト表示および新規作成
class ItemView(APIView):

        # リクエストメソッドごとに認証クラスを設定
    def get_authenticators(self):
        if self.request.method == "POST":
            return []
        else:
            return [CustomJWTAuthentication]

    # リクエストメソッドごとにパーミッションクラスを設定
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny]
        else:
            return  [IsAuthenticated]
 
    #fアイテムリスト表示
    def get(self, request, user_id, list_id):
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    # アイテム新規作成
    def post(self, request, user_id, list_id):
        # リクエストデータとlist_idを使って新しいアイテムを作成
        serializer = ItemCreateSerializer(data=request.data)
        # list_idを使ってListインスタンスを取得し、アイテムを保存
        if serializer.is_valid():
            list_instance = List.objects.get(pk=list_id) 
            serializer.save(list_id=list_instance)
        # 作成、保存されたアイテムをシリアライズして返す
            response_serializer = ItemResponseSerializer(serializer.instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
