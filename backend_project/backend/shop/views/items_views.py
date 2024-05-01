from django.shortcuts import render
from rest_framework import generics
from ..models import Item
from ..serializers.items_serializers import ItemSerializer
from django.db.models import Q

# Create your views here.
# アイテムリスト（表示）
class ItemList(generics.ListCreateAPIView):
    #queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        list_id = self.kwargs.get('list_id')
        # (owner または invitee) かつ list_id__id=list_id の条件でフィルタリング
        return Item.objects.filter(
            Q(list_id__owner_id=user_id) | 
            Q(list_id__members__invitee_id=user_id),
            list_id=list_id
        )
    
                                   

    
# アイテムリスト（新規作成）

# アイテムリスト（更新）
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# アイテムリスト（削除）