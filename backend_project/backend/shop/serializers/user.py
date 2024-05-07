from rest_framework import serializers
from shop.models import User, List


"""
SignupSerializer
ユーザー登録処理に使用するSerializer
"""
class SignupSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    user_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

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
GetUpdateUserSerializer
ユーザー情報表示に使用するSerializer
"""
class GetUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "user_name", "email", "password", "line_id",
                  "line_status", "user_icon", "invitation", "request",
                  "have_list", "default_list", "remind", "remind_timing",
                  "remind_time"]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ["user_id", "line_id"]

    # レスポンスに含めるデータを制御
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get("request")
        if request and request.method == "PATCH":
            fields = request.data.keys()
            ret = {field: value for field, value in ret.items() if field in fields
            }
        return ret