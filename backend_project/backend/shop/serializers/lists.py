from rest_framework import serializers
from ..models import List, Item, Members

# 買い物リスト表示用
# Itemモデルからもってくるフィールド
class ListItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ('item_id', 'item_name', 'color', 'last_purchase_at', 'link', 'to_list',)

class ListSerializer(serializers.ModelSerializer):
    # Itemモデルから持ってきたもののserializerをネストする
    items = ListItemSerializer(many=True, read_only=True)
    authority = serializers.SerializerMethodField()
    
    class Meta:
        model = List
        fields = ('list_id', 'list_name', 'authority', 'items',)
    # アクセスしているユーザーのuser_idが含まれるMembersのレコードからauthority を取得
    def get_authority(self, obj):
        # requestオブジェクトを取得
        request = self.context.get('request')
        # requestから、ログインしているユーザーのuser_idを取得
        user_id = request.user.id if request and request.user else None

        # user_idが含まれるMembersレコードからauthorityを取得
        if user_id:
            member = Members.objects.filter(list=obj, invitee_id=user_id).first()
            if member:
                return member.authority
            return None
        



