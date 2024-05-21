from django.contrib.auth import authenticate
from rest_framework import serializers
from shop.models import User


"""
LoginSerializer
ログイン処理の認証に使用するSerializer
"""
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    # 受取ったemailとpasswordでユーザー認証
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                return {"user": user}
            else:
                raise serializers.ValidationError("ユーザーは存在しません")
        else:
            raise serializers.ValidationError("メールアドレスとパスワードを入力してください")


"""
LoginResponseSerializer
ログイン処理のレスポンスに使用するSerializer
"""
class LoginResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "user_name", "email", "line_id", "line_status",
                  "user_icon", "invitation", "request", "have_list",
                  "default_list", "remind", "remind_timing", "remind_time"]
