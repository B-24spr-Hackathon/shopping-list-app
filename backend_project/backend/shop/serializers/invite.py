from rest_framework import serializers
from shop.models import  User, Member


# 招待者情報取得用
class FindUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user_id', 'user_name', 'user_icon')

