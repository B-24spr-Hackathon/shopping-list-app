from rest_framework import serializers
from shop.models import  List, Item
from rest_framework .exceptions import ValidationError


# リスト設定リクエスト用
class ListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('list_name', 'shopping_cycle', 'shopping_day', 'day_of_week',)

    def validate(self, data):
        # 買い物頻度に基づく要追加入力項目の設定
        shopping_cycle = data.get('shopping_cycle')
        shopping_day = data.get('shopping_day')
        day_of_week = data.get('day_of_week')
        # 買い物頻度が毎月の場合、買い物日要入力
        if shopping_cycle == 0:
            if shopping_day is None:
                raise ValidationError({'shopping_day': 'この項目は入力必須です'})
        # 買い物頻度が隔週または毎週の場合、買い物曜日要入力   
        elif shopping_cycle in [1, 2]:
            if day_of_week is None:
                raise ValidationError({'day_of_week': 'この項目は入力必須です'})
            
        return data
        
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

    def validate(self, data):
        # 買い物頻度に基づく要追加入力項目の設定
        shopping_cycle = data.get('shopping_cycle')
        shopping_day = data.get('shopping_day')
        day_of_week = data.get('day_of_week')
        # 買い物頻度が毎月の場合、買い物日要入力
        if shopping_cycle == 0:
            if shopping_day is None:
                raise ValidationError({'shopping_day': 'この項目は入力必須です'})
        # 買い物頻度が隔週または毎週の場合、買い物曜日要入力   
        elif shopping_cycle in [1, 2]:
            if day_of_week is None:
                raise ValidationError({'day_of_week': 'この項目は入力必須です'})
            
        return data
