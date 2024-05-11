from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
import requests, jwt
from shop.serializers.line import LineSignupSerializer, LineLoginSerializer
from shop.models import User
from shop.serializers.login import LoginResponseSerializer


# LINEログインで使用するパラメーターを定義
client_id = settings.LINE_CHANNEL_ID
client_secret = settings.LINE_CHANNEL_SECRET
redirect_uri = settings.REDIRECT_URL
state = settings.STATE

# フロントエンドへのリダイレクト先
redirect_ok = settings.FRONT_REDIRECT_URL
redirect_ng = settings.FRONT_ERROR_URL

"""
LineCallbackView
LINE認証サーバーからのコールバックに対応するView
"""
class LineCallbackView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        # クエリパラメータから認可コードなどを取得
        code = request.GET.get("code")
        state = request.GET.get("state")
        error = request.GET.get("error")
        error_description = request.GET.get("error_description")
        status = request.GET.get("friendship_status_changed")

        # errorが発生しているか確認
        if error:
            return redirect(f"{redirect_ng}?error={error}&error_description={error_description}")

        # stateの値の確認（csrf防止のため）
        if state != settings.STATE:
            return redirect(f"{redirect_ng}?error=bad_request")

        # アクセストークンを受取るための情報定義
        token_url = "https://api.line.me/oauth2/v2.1/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret
        }

        # POSTリクエストを送信しアクセストークンを取得
        response = requests.post(token_url, headers=headers, data=data)
        tokens = response.json()
        if response.status_code != 200:
            return redirect(f"{redirect_ng}?error={response.status_code}&error_msg={response.text}")

        # id_token(JWT)からユーザー情報を取得
        id_token = tokens["id_token"]
        payload = jwt.decode(id_token, client_secret, audience=client_id,
                             issuer="https://access.line.me",
                             algorithms=["HS256"])

        # id_tokenからユーザー情報を取得
        user_name = payload["name"]
        line_id = payload["sub"]

        # ユーザーがDBに存在する場合
        if User.objects.filter(line_id=line_id).exists():
            return redirect(f"{redirect_ok}?line_id={line_id}")

        # ユーザーがDBに存在しない場合
        return redirect(
            f"{redirect_ok}?line_id={line_id}&user_name={user_name}&status={status}"
        )


"""
LineSignupView
LINEログインからユーザーを登録するためのView
"""
class LineSignupView(APIView):
    authentication_classes = []
    permission_classes = []

    # POSTリクエストの処理（登録）
    def post(self, request):
        serializer = LineSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = AccessToken.for_user(user)
            return Response({
                "user": serializer.data,
                "access": str(token)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
LineLoginView
LINEログインからログインするためのView
"""
class LineLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    # POSTリクエストの処理
    def post(self, request):
        serializer = LineLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token = AccessToken.for_user(user)
            response_serializer = LoginResponseSerializer(user)
            return Response({
                "user": response_serializer.data,
                "access": str(token)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
LineLinkView
LINE連携に対応するView
"""
class LineLinkView(APIView):
    def get(self, request):
        user = request.user
        secret = settings.SECRET_KEY
        channel_url = settings.CHANNEL_URL
        
        # JWTを生成するためのペイロードを定義
        payload = {
            "user_id": user.user_id,
            "exp": datetime.now() + timedelta(minutes=10),
            "iat": datetime.now()
        }
    
        # JWTの生成
        token = jwt.encode(payload, secret, algorithm="HS256")
        
        return Response({
                "url": channel_url,
                "otp": str(token)
            }, status=status.HTTP_200_OK)