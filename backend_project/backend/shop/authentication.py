from rest_framework import authentication, exceptions
import jwt
from django.conf import settings
from shop.models import User
import logging

logger = logging.getLogger("backend")


"""
CustomJWTAuthentication
JWTを使用した認証の定義
"""
class CustomJWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        logger.info("JWT認証の開始")
        # CookieからJWTを取得
        token = request.COOKIES.get(settings.SIMPLE_JWT["COOKIE_NAME"])
        if not token:
            logger.error("トークンが存在しない")
            raise exceptions.AuthenticationFailed("トークンが存在しません")

        # JWTを検証
        try:
            payload = jwt.decode(
                token,
                settings.SIMPLE_JWT["SIGNING_KEY"],
                algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
            )
        except jwt.InvalidTokenError:
            logger.error("トークンが無効")
            raise exceptions.AuthenticationFailed("トークンが無効です")

        # JWTのペイロードからユーザーを取得
        try:
            user_id_field = settings.SIMPLE_JWT["USER_ID_FIELD"]
            user_id = payload[settings.SIMPLE_JWT["USER_ID_CLAIM"]]
            user = User.objects.get(**{user_id_field: user_id})
        except User.DoesNotExist:
            logger.error("ユーザーがDBに存在しない")
            raise exceptions.AuthenticationFailed("ユーザーが見つかりません")

        logger.info("JWT認証の終了")
        return (user, None)


"""
user_authentication_rule
JWTでユーザーを認証する際に使用するルール
DBにユーザーが存在すれば認証
"""
def user_authentication_rule(user):
    return user is not None