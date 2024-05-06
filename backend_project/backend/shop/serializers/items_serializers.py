from rest_framework import serializers
from ..models import Item

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('list_id', 'item_id', 'item_name', 'color', 'consume_cycle', 'last_purchase_at', 'last_open_at', 'link', 'to_list', 'remind_by_item', 'manage_target', )


