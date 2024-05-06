from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import List
from shop.authentication import CustomJWTAuthentication
from shop.serializers.lists import ShoppingListSerializer, ListCreateSerializer, ListResponseSerializer, ListUpdateSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404


# 買い物リスト表示(GET)
class ShoppingListView(APIView):
    # JWT認証を要求する
    permission_classes = [IsAuthenticated]  
    def get(self, request, list_id):
        # ownerまたはinvitee、かつlist_idでリストをフィルタリング
        filters = (Q(owner_id=request.user) | Q(members__invitee_id=request.user)) & Q(list_id=list_id)
        # 対象のリストを取得
        lists = List.objects.filter(filters)
        # リストが見つからない場合エラーを返す
        if not lists.exists():
            return Response({"message": "リストが見つからないか、アクセス権限がありません。"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ShoppingListSerializer(lists, many=True)
        return Response(serializer.data)
    

class ListView(APIView):
    # JWT認証を要求する
    permission_classes = [IsAuthenticated]

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
        # オーナーのみフィルタリング
        list_instance = get_object_or_404(List, pk=list_id, owner_id=request.user)

        serializer = ListResponseSerializer(list_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # リスト設定（更新）PATCH
    def patch(self, request, list_id):
        # オーナーのみフィルタリング
        list_instance = get_object_or_404(List, pk=list_id, owner_id=request.user)

        serializer = ListUpdateSerializer(list_instance, data=request.data, context={"request":request}, partial=True)

        if serializer.is_valid():
            saved_list = serializer.save()
            update_serializer = ListUpdateSerializer(saved_list)
            return Response(update_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                   
    # リスト設定（削除）DELETE
    def delete(self, request, list_id):
        # オーナーのみフィルタリング
        list_instance = get_object_or_404(List, pk=list_id, owner_id=request.user)
        # 削除する前にシリアライズしたデータを保存
        response_serializer = ListResponseSerializer(list_instance)
        serialized_data = response_serializer.data

        list_instance.delete()

        return Response(serialized_data, status=status.HTTP_200_OK)