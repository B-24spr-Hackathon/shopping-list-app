from rest_framework import serializers
from shop.models import  User


# 招待者情報取得 
class FindUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user_id', 'user_name', 'user_icon')
        


