from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests, jwt, base64, hashlib, hmac
from shop.models import User, List, Item
from shop.serializers.user import GetUpdateUserSerializer
from shop.serializers.webhook import ItemSerializer


# デフォルトの値を定義
client_secret = settings.LINE_CHANNEL_SECRET
secret = settings.SECRET_KEY
access_token = settings.CHANNEL_ACCESS_TOKEN
reply_url = settings.REPLY_URL
redirect_url = settings.LINK_REDIRECT_URL

# メッセージ送信用ヘッダーの定義
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

"""
LineWebhookView
LINEのWebhookに対応するView
"""
class LineWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    # POSTリクエストで届くWebhookイベントの処理
    def post(self, request):
        # 署名の検証
        line_signature = request.headers.get("x-line-signature")
        body = request.body
        hash = hmac.new(client_secret.encode("utf-8"),
                        body, hashlib.sha256).digest()
        signature = base64.b64decode(hash).decode("utf-8")
        if not hmac.compare_digest(signature, line_signature):
            return Response({"error": "Invalid signature"},
                            status=status.HTTP_400_BAD_REQUEST)

        # リクエストボディからeventsを取得
        events = request.data.get("events")

        # 取得したeventsを1つずつ処理
        for event in events:

            # メッセージを受取った時の処理
            if event["type"] == "message":
                reply_token = event["replyToken"]

                # 受取ったメッセージがtextの時の処理
                if event["message"]["type"] == "text":
                    text = event["message"]["text"]
                    user_id = verify_jwt(text)

                    # メッセージがjwtの時の処理（line_id, line_statusをDBに保存）
                    if user_id:
                        line_id = event["source"]["userId"]
                        user = User.objects.get(user_id=user_id)
                        serializer = GetUpdateUserSerializer(user,
                            data={"line_id": line_id, "line_status": True}, partial=True)

                        # line_idをDBに保存出来た時の処理
                        if serializer.is_valid():
                            serializer.save()
                            user_name = serializer.data["user_name"]
                            data = {
                                "replyToken": reply_token,
                                "messages": {
                                    "type": "text",
                                    "text": f"{user_name}さん\n友達追加ありがとうございます！\nアプリへ戻って設定の続きをお願いします\n\n{redirect_url}"
                                }
                            }

                            # リダイレクトURLの送信
                            response = requests.post(reply_url, headers=headers, json=data)
                            if response.status_code != 200:
                                print(f"連携の返信メッセージ送信エラー: {response.status_code}, {response.text}")

                        # line_idをDBに保存できなかった時の処理
                        else:
                            print(f"line_id保存エラー")

                    # メッセージがjwt以外の時の処理
                    else:
                        data = {
                            "replyToken": reply_token,
                            "messages": {
                                "type": "text",
                                "text": "メッセージありがとうございます！\n買いもっとでは通知のみを行っており、メッセージは受付けておりません m _ _ m"
                            }
                        }

                        # 対応していない旨のメッセージ送信
                        response = requests.post(reply_url, headers=headers, json=data)
                        if response.status_code != 200:
                            print(f"連携以外の返信メッセージ送信エラー: {response.status_code}, {response.text}")

                # text以外のメッセージに対する処理
                else:
                    data = {
                        "replyToken": reply_token,
                        "messages": {
                            "type": "text",
                            "text": "ありがとうございます！\n買いもっとでは通知のみを行っており、メッセージは受付けておりません m _ _ m",
                        },
                    }

                    # 対応していない旨のメッセージ送信
                    response = requests.post(reply_url, headers=headers, json=data)
                    if response.status_code != 200:
                        print(f"text以外の返信メッセージ送信エラー: {response.status_code}, {response.text}")

            # 友達登録解除の時の処理
            elif event["type"] == "unfollow":
                line_id = event["source"]["userId"]
                user = User.objects.get(line_id=line_id)

                # usersテーブルのline_status, remindをfalseに変更
                serializer = GetUpdateUserSerializer(user,
                    data={"line_status": False, "remind": False}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print("友達解除でのline_status保存エラー")

                # itemsテーブルの関係するitemのremind_by_itemをfalseに設定
                lists = List.objects.filter(owner_id=user_id)
                items = Item.objects.filter(list_id__in=lists)
                for item in items:
                    serializer = ItemSerializer(item, data={"remind_by_item": False}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        print(f"友達解除でのremind_by_item保存エラー: {item.item_id}")

            # 友達登録時の処理
            elif event["type"] == "follow":
                reply_token = event["replyToken"]
                line_id = event["source"]["userId"]
                user = User.objects.get(line_id=line_id)

                # usersテーブルのline_statusをtrueに変更
                serializer = GetUpdateUserSerializer(
                    user, data={"line_status": True}, partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                else:
                    print("友達登録でのline_status保存エラー")

                # メッセージの送信
                data = {
                    "replyToken": reply_token,
                    "messages": {
                        "type": "text",
                        "text": "友だち追加ありがとうございます！\n買いもっとからの通知をお待ちください m _ _ m",
                    },
                }

                response = requests.post(reply_url, headers=headers, json=data)
                if response.status_code != 200:
                    print(f"友達登録の返信メッセージ送信エラー: {response.status_code}, {response.text}")

            # postback（ユーザーか通知に対して起こしたリアクション）の処理
            elif event["type"] == "postback":
                reply_token = event["replyToken"]
                line_id = event["source"]["userId"]
                user = User.objects.get(line_id=line_id)

                data = event["postback"]["data"]

                # アイテムを買い物リストに追加する時の処理
                if type(data) == int:
                    item = Item.objects.get(item_id=data)
                    serializer = ItemSerializer(item, data={"to_list": True}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        print("アイテムのto_list保存エラー")

                    # メッセージの送信
                    data = {
                        "replyToken": reply_token,
                        "messages": {
                            "type": "text",
                            "text": f"{item.item_name}を追加しました",
                        },
                    }

                    response = requests.post(reply_url, headers=headers, json=data)
                    if response.status_code != 200:
                        print(f"買い物リストに追加した時の返信メッセージ送信エラー: {response.status_code}, {response.text}")

                # アイテムを買い物リストに追加しない時の処理
                else:
                    # メッセージの送信
                    data = {
                        "replyToken": reply_token,
                        "messages": {
                            "type": "text",
                            "text": f"{data}を追加しませんでした",
                        },
                    }

                    response = requests.post(reply_url, headers=headers, json=data)
                    if response.status_code != 200:
                        print(
                            f"買い物リストに追加しなかった時の返信メッセージ送信エラー: {response.status_code}, {response.text}"
                        )

        # eventsの処理が完了したらOKレスポンスを返す
        return Response(status=status.HTTP_200_OK)


"""
verify_jwt
jwtを検証、データを抽出する関数
"""
def verify_jwt(text):
    try:
        payload = jwt.decode(text, secret, algorithms=["HS256"])
        user_id = payload["user_id"]
        return user_id
    except Exception:
        return False
