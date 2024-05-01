from rest_framework import serializers
from ..models import Item

class ItemSerializer(serializers.ModelSerializer):
    list_name = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('list_id', 'list_name', 'item_id','item_name', 'color', 'consume_cycle', 'last_purchase_at', 'last_open_at', 'link', 'to_list', 'remind_by_item', 'manage_target', )

    # list_name をListモデルから取得する
    def get_list_name(self, obj):
        return obj.list_id.list_name
