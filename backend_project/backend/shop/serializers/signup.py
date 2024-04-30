from rest_framework import serializers
from shop.models import User


"""
UserRegisterSerializer
ユーザー登録処理に使用するSerializer
"""
class SignupSerializer(serializers.Serializer):
    user_id = serializers.CharField(write_only=True, required=True)
    user_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    # user_idの確認
    def validate_user_id(self, value):
        user = User(user_id=value)
        if user:
            raise serializers.ValidationError("登録済みのIDです")
        return value
    
    # emailの確認
    def validate_email(self, value):
        user = User(email=value)
        if user:
            raise serializers.ValidationError("登録済みのメールアドレスです")
        return value