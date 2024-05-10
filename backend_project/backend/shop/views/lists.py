from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import List
from shop.authentication import CustomJWTAuthentication
from shop.serializers.lists import ListCreateSerializer, ListResponseSerializer, ListUpdateSerializer
from django.shortcuts import get_object_or_404
from shop.permissions import IsOwner

class ListView(APIView):
    # JWT認証を要求、オーナーのみ許可
    permission_classes = [IsAuthenticated, IsOwner]
    # POSTメソッドだけは誰でも可
    def get_permission(self):
       if self.request.method == 'POST':
           return [IsAuthenticated()] 
       return [IsAuthenticated(), IsOwner()]

    # リスト設定（登録）POST
    def post(self, request):
        serializer = ListCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner_id=request.user)
            response_serializer = ListResponseSerializer(serializer.instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # リスト設定（表示）GET
    def get(self, request, list_id):
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)

        serializer = ListResponseSerializer(list_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # リスト設定（更新）PATCH
    def patch(self, request, list_id):
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)

        serializer = ListUpdateSerializer(list_instance, data=request.data, context={"request":request}, partial=True)

        if serializer.is_valid():
            # データベースのデータを更新して保存
            serializer.save()
            # 更新されたフィールドのみを辞書として取得
            update_fields = {field: request.data[field] for field in request.data}
            # 更新されたフィールドのみをレスポンスとして返す
            return Response(update_fields, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                   
    # リスト設定（削除）DELETE
    def delete(self, request, list_id):
        # リストを取得
        list_instance = get_object_or_404(List, pk=list_id)
        # パーミッションチェックを実行
        self.check_object_permissions(self.request, list_instance)
        # 削除する前にシリアライズしたデータを保存
        response_serializer = ListResponseSerializer(list_instance)
        serialized_data = response_serializer.data

        list_instance.delete()

        return Response(serialized_data, status=status.HTTP_200_OK)