from rest_framework import serializers
from shop.models import User


"""
LineSignupSerializer
LINEログインでユーザー登録に使用するSerializer
"""
class LineSignupSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    user_name = serializers.CharField()
    line_id = serializers.CharField()
    email = serializers.EmailField(required=False)

    def create(self, validated_data):
        user_id = validated_data["user_id"]
        email = user_id + "@shopping.com"
        validated_data["email"] = validated_data.get("email", email)
        return User.objects.create_user(**validated_data)

    # user_idがDBに存在するか確認
    def validate_user_id(self, value):
        if User.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("登録済みのuser_idです")
        return value

    # line_idがDBに存在するか確認
    def validate_line_id(self, value):
        if User.objects.filter(line_id=value).exists():
            raise serializers.ValidationError("登録済みのline_idです")
        return value


"""
LineLoginSerializer
LINEログインでログインに使用するSerializer
"""
class LineLoginSerializer(serializers.Serializer):
    line_id = serializers.CharField()
    
    # 受取ったline_idでユーザー認証
    def validate(self, data):
        line_id = data.get("line_id")
        if User.objects.filter(line_id=line_id).exists():
            user = User.objects.get(line_id=line_id)
            return {"user": user}
        else:
            raise serializers.ValidationError("ユーザーは存在しません")
