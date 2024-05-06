from django.shortcuts import render
from rest_framework import generics
from ..models import Item
from ..serializers.items_serializers import ItemSerializer
from django.db.models import Q

# Create your views here.

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# user_idとlist_idで表示する情報をフィルタリング
# user_idは外部キーであるownerまたはinviteeから取得



class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

