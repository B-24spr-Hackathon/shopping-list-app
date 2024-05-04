from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
import requests, jwt
from shop.serializers.line import LineSerializer
from shop.models import User


# LINEログインで使用するパラメーターを定義
client_id = settings.LINE_CHANNEL_ID
client_secret = settings.LINE_CHANNEL_SECRET
redirect_uri = settings.REDIRECT_URL
state = settings.STATE

"""
"""
class LineLoginView(APIView):
    authentication_classes = []

    # POSTリクエストの処理
    def post(self, request):
        # 受取ったuser_idをDBへ保存
        serializer = LineSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = AccessToken.for_user(user)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
        # 上記以外のLINEログイン用パラメータを設定
        scope = "profile%20openid"
        user_id = serializer.data["user_id"]

        # LINE認証サーバーのURL生成
        line_url = f"https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}"
        
        # LINE認証サーバーへのリクエストURLの返信
        return Response({
            "user_id": user_id,
            "access": str(token),
            "url": line_url
            }, status=status.HTTP_200_OK)


class LineCallbackView(APIView):
    authentication_classes = []

    def get(self, request, parameter):
        # クエリパラメータから認可コードを取得
        code = request.GET.get("code")
        get_state = request.GET.get("state")
        if get_state != state:
            return Response()
            # return redirect("http://0.0.0.0:5173/home", error="不適切なアクセスです")
        error = request.GET.get("error")
        if error:
            return redirect("http://0.0.0.0:5173/home", error="LINE認証過程でエラーが発生しました")

        # アクセストークンを受取るリクエストのための情報定義
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
        if response.status_code == 200:
            # 取得した情報を辞書型に変換
            tokens = response.json()
            if "error" in tokens:
                return redirect("http://0.0.0.0:5173/home",
                                error="トークンの取得に失敗しました")
        else:
            return redirect("http://0.0.0.0:5173/home",
                            error="トークンの取得に失敗しました")

        # JWTであるid_tokenを取得
        id_token = tokens["id_token"]
        decoded_token = jwt.decode(id_token, client_secret, audience=client_id,
                                   issuer="https://access.line.me",
                                   algorithms=["HS256"])

        # id_tokenからユーザー情報を取得
        user_name = decoded_token["name"]
        line_id = decoded_token["sub"]

        # パスパラメーターからuser_idを取得
        user_id = parameter
        user = User.objects.get(user_id=user_id)
        serializer = LineSerializer(user,
                                    data={"user_name": user_name,
                                          "line_id": line_id},
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            token = AccessToken.for_user(user)
            return Response({
                "user": serializer.data,
                "access": str(token)
            })
            # return redirect("http://0.0.0.0:5173/home", user_id=user_id)

        return Response({})
        # return redirect("http://0.0.0.0:5173/home", error="user_idが存在しません")
