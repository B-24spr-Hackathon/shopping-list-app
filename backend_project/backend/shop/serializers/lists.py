from rest_framework import serializers
from shop.models import  List, Item


# 買い物リスト表示用

# Itemモデルからもってくるフィールド
class ListItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ('item_id', 'item_name', 'color', 'last_purchase_at', 'link', 'to_list',)

class ShoppingListSerializer(serializers.ModelSerializer):    
    items = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = ('list_id', 'list_name', 'items',)
    # to_list=Trueだけを表示する
    def get_items(self, obj):
        items = Item.objects.filter(list_id=obj, to_list=True)
        return ListItemSerializer(items, many=True).data

# リスト設定リクエスト用
class ListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('list_name', 'shopping_cycle', 'shopping_day', 'day_of_week',)

# リスト設定（表示）（登録）（更新）(削除)レスポンス用
class ListResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('list_id', 'list_name', 'shopping_cycle', 'shopping_day', 'day_of_week',)
      
# リスト更新リクエスト、レスポンス用      
class ListUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('list_name', 'shopping_cycle', 'shopping_day', 'day_of_week',)