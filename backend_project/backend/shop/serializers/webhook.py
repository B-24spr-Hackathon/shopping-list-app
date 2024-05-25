from rest_framework import serializers
from shop.models import Item


"""
ItemSerializer
itemの処理を担当するSerializer
"""
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["item_id", "remind_by_item", "to_list", "last_open_at",
                  "consume_cycle"]
        read_only_fields = ["item_id"]