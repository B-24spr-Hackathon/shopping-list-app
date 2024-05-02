from rest_framework import serializers
from shop.models import User, List


"""
SignupSerializer
ユーザー登録処理に使用するSerializer
"""
class SignupSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    user_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # DBへユーザーを保存（save()メソッドが呼出された時に実行される）
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    # user_idがDBに存在するか確認
    def validate_user_id(self, value):
        if User.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("登録済みのIDです")
        return value

    # emailがDBに存在するか確認
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("登録済みのメールアドレスです")
        return value


"""
GetUserSerializer
ユーザー情報表示に使用するSerializer
"""
class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "user_name", "email", "line_id", "user_icon",
                  "invitation", "request", "have_list", "default_list",
                  "remind", "remind_timing", "remind_time"]
