from rest_framework import serializers
from shop.models import Item

# 買い物リスト表示用
class ShoppingListSerializer(serializers.ModelSerializer):   

    class Meta:
        model = Item
        fields = ('item_id', 'item_name', 'color', 'last_purchase_at', 'item_url', 'to_list',)
