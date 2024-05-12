from rest_framework import serializers
from shop.models import  List


# リスト設定リクエスト,更新リクエスト、更新レスポンス用  
class ListCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('list_name', 'shopping_day',)
        
# リスト設定　表示、登録、削除レスポンス用
class ListResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('list_id', 'list_name', 'shopping_day', )
      

