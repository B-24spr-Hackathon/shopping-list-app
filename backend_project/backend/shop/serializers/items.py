from rest_framework import serializers
from ..models import Item

# アイテムリスト表示用
class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('item_id', 'item_name', 'color', 'consume_cycle', 'last_purchase_at', 'last_open_at', 'item_url', 'to_list', 'remind_by_item', 'manage_target')

# アイテムリスト作成リクエスト用
class ItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('item_name', 'color', 'consume_cycle', 'last_purchase_at', 'last_open_at', 'item_url', 'remind_by_item', )

# アイテムリスト作成レスポンス用、更新レスポンス用、削除レスポンス用
class ItemResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('item_id', 'item_name', 'list_id', 'color', 'consume_cycle', 'last_purchase_at', 'last_open_at', 'item_url', 'to_list', 'remind_by_item', 'manage_target',)

# アイテム更新リクエスト用
class ItemUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('item_name', 'color', 'consume_cycle', 'last_purchase_at', 'last_open_at', 'item_url',  'remind_by_item', 'manage_target',)

