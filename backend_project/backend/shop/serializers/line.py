from rest_framework import serializers
from shop.models import User


class LineSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    user_name = serializers.CharField(required=False)
    line_id = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def create(self, validated_data):
        user_id = validated_data["user_id"]
        email = user_id + "@shopping.com"
        validated_data["email"] = validated_data.get("email", email)
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.user_name = validated_data.get("user_name",
                                                instance.user_name)
        instance.line_id = validated_data.get("line_id", instance.line_id)
        instance.save()
        return instance

    # user_idがDBに存在するか確認
    def validate_user_id(self, value):
        if User.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("登録済みのIDです")
        return value
