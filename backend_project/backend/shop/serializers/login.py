from django.contrib.auth import authenticate
from rest_framework import serializers
from shop.models import User


"""
LoginSerializer
ログイン処理の認証に使用するSerializer
"""
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    # emailがDBに登録されているか確認
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return value
        else:
            return serializers.ValidationError("メールアドレスが登録されていません")

    # 受取ったemailとpasswordでユーザー認証
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                return {"user": user}
            else:
                raise serializers.ValidationError("パスワードが違います")
        else:
            raise serializers.ValidationError("エラー")


"""
LoginResponseSerializer
ログイン処理のレスポンスに使用するSerializer
"""
class LoginResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "user_name", "email", "line_id", "user_icon",
                "invitation", "request", "have_list", "default_list", "remind",
                "remind_timing", "remind_time"]
