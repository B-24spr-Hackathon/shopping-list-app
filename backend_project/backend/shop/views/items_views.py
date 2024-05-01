from django.shortcuts import render
from rest_framework import generics, status
from ..models import Item, List
from ..serializers.items_serializers import ItemSerializer, ItemCreateSerializer, ItemRetrieveSerializer
from django.db.models import Q
from rest_framework.response import Response


# アイテムリスト表示および新規作成
class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

   # 同じビューを利用して新規作成POST
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ItemCreateSerializer
        return ItemSerializer
    
    # 同じビューを利用して表示GET
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        list_id = self.kwargs.get('list_id')

        # (owner または invitee) かつ list_id__id=list_id の条件でフィルタリング
        return Item.objects.filter(
            Q(list_id__owner_id=user_id) | 
            Q(list_id__members__invitee_id=user_id),
            list_id=list_id
        ) 
    # urlからlist_id を取得してPost
    def perform_create(self, serializer):
        list_id = self.kwargs.get('list_id')
        list_instance = List.objects.get(pk=list_id) 
        serializer.save(list_id=list_instance)

    # POSTへのレスポンスのカスタマイズ
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 詳細情報表示に利用するserializer設定
        retrieve_serializer = ItemRetrieveSerializer(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
