from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests, jwt, base64, hashlib, hmac, json
from shop.models import User, List, Item
from shop.serializers.user import GetUpdateUserSerializer
from shop.serializers.webhook import ItemSerializer
from shop.views.items import CheckCycle
import logging

logger = logging.getLogger("backend")


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
        request_body = request.body
        request_data = json.loads(request_body.decode("utf-8"))
        logger.info(f"{request.method}:{request.build_absolute_uri()}")
        logger.info(f"{request_data}")

        logger.info("Webhook処理開始")
        # 署名の検証
        line_signature = request.headers.get("x-line-signature")
        body = request.body
        hash = hmac.new(client_secret.encode("utf-8"),
                        body, hashlib.sha256).digest()
        signature = base64.b64encode(hash).decode("utf-8")
        if not hmac.compare_digest(signature, line_signature):
            logger.error("署名検証の失敗")
            return Response({"error": "Invalid signature"},
                            status=status.HTTP_400_BAD_REQUEST)

        # リクエストボディからeventsを取得
        events = request_data.get("events")

        # 取得したeventsを1つずつ処理
        for event in events:

            # メッセージを受取った時の処理
            if event["type"] == "message":
                reply_token = event["replyToken"]

                # 受取ったメッセージがtextの時の処理
                if event["message"]["type"] == "text":
                    # メッセージ文がJWTか確認
                    text = event["message"]["text"]
                    user_id = verify_jwt(text)

                    # メッセージがjwtの時の処理（line_id, line_statusをDBに保存）
                    if isinstance(user_id, str):
                        logger.info(f"JWTの受信(user_id: {user_id})")
                        line_id = event["source"]["userId"]
                        user = User.objects.get(user_id=user_id)
                        serializer = GetUpdateUserSerializer(user,
                            data={"line_id": line_id, "line_status": True}, partial=True)

                        # line_idをDBに保存出来た時の処理
                        if serializer.is_valid():
                            logger.info("line_id, line_statusの保存成功")
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
                            if response.ok:
                                logger.info("LINE連携通知成功")
                            else:
                                logger.error(f"LINE連携通知失敗: {response.text}")

                        # line_idをDBに保存できなかった時の処理
                        else:
                            logger.error("line_idの保存失敗")

                    # メッセージがjwt以外の時の処理
                    else:
                        logger.info(f"JWT以外のtext受信(user_id: {user_id})")
                        data = {
                            "replyToken": reply_token,
                            "messages": {
                                "type": "text",
                                "text": "メッセージありがとうございます！\n買いもっとでは通知のみを行っており、メッセージは受付けておりません m _ _ m"
                            }
                        }

                        # 対応していない旨のメッセージ送信
                        response = requests.post(reply_url, headers=headers, json=data)
                        if response.ok:
                            logger.info("定型文送信成功")
                        else:
                            logger.error(f"定型文送信失敗: {response.text}")

                # text以外のメッセージに対する処理
                else:
                    logger.info("text以外の受信")
                    data = {
                        "replyToken": reply_token,
                        "messages": {
                            "type": "text",
                            "text": "ありがとうございます！\n買いもっとでは通知のみを行っており、メッセージは受付けておりません m _ _ m",
                        },
                    }

                    # 対応していない旨のメッセージ送信
                    response = requests.post(reply_url, headers=headers, json=data)
                    if response.ok:
                        logger.info("定型文送信成功")
                    else:
                        logger.error(f"定型文送信失敗: {response.text}")

            # 友達登録解除の時の処理
            elif event["type"] == "unfollow":
                line_id = event["source"]["userId"]
                user = User.objects.get(line_id=line_id)

                logger.info(f"友達登録解除の受信(user_id: {user.user_id})")

                # usersテーブルのline_status, remindをfalseに変更
                serializer = GetUpdateUserSerializer(user,
                    data={"line_status": False, "remind": False}, partial=True)
                if serializer.is_valid():
                    logger.info("remind, line_status更新成功")
                    serializer.save()
                else:
                    logger.error("remind, line_status更新失敗")

                # itemsテーブルの関係するitemのremind_by_itemをfalseに設定
                lists = List.objects.filter(owner_id=user.user_id)
                items = Item.objects.filter(list_id__in=lists)
                for item in items:
                    serializer = ItemSerializer(item, data={"remind_by_item": False}, partial=True)
                    if serializer.is_valid():
                        logger.info("remind_by_itemの更新成功")
                        serializer.save()
                    else:
                        logger.error(f"remind_by_itemの更新失敗: {response.text}")

            # 友達登録時の処理
            elif event["type"] == "follow":
                reply_token = event["replyToken"]
                line_id = event["source"]["userId"]
                user = User.objects.get(line_id=line_id)

                logger.info(f"友達登録の受信(user_id: {user.user_id})")

                # usersテーブルのline_statusをtrueに変更
                serializer = GetUpdateUserSerializer(
                    user, data={"line_status": True}, partial=True
                )
                if serializer.is_valid():
                    logger.info("line_statusの更新成功")
                    serializer.save()
                else:
                    logger.error("line_statusの更新失敗")

                # メッセージの送信
                data = {
                    "replyToken": reply_token,
                    "messages": {
                        "type": "text",
                        "text": "友だち追加ありがとうございます！\n買いもっとからの通知をお待ちください m _ _ m",
                    },
                }

                response = requests.post(reply_url, headers=headers, json=data)
                if response.ok:
                    logger.info("友達登録の返信成功")
                else:
                    logger.error(f"友達登録の返信失敗: {response.text}")

            # postback（ユーザーか通知に対して起こしたリアクション）の処理
            elif event["type"] == "postback":
                reply_token = event["replyToken"]
                line_id = event["source"]["userId"]
                user = User.objects.get(line_id=line_id)

                logger.info(f"postbackの受信(user_id: {user.user_id})")

                data = event["postback"]["data"]

                # アイテムを買い物リストに追加する時の処理
                if type(data) == int:
                    item = Item.objects.get(item_id=data)
                    # to_listがすでにTrueの場合はその旨をLINE通知
                    if item.to_list:
                        # メッセージの送信
                        data = {
                            "replyToken": reply_token,
                            "messages": {
                                "type": "text",
                                "text": f"{item.item_name}は既に追加済みです",
                            },
                        }

                        response = requests.post(reply_url, headers=headers, json=data)
                        if response.ok:
                            logger.info("買い物リスト追加済み通知の送信成功")
                        else:
                            logger.error(f"買い物リスト追加済み通知の送信失敗: {response.text}")
                    
                    # to_listがFalseの場合
                    else:
                        today = timezone.now().date()

                        new_cycle = CheckCycle(item.consume_cycle, item.last_open_at)

                        # 消費頻度の更新が必要な場合
                        if new_cycle:
                            serializer = ItemSerializer(
                                item,
                                data={"to_list": True, "last_open_at": today,
                                    "consume_cycle": new_cycle},
                                partial=True,
                            )
                        # 消費頻度の更新が不要な場合
                        else:
                            serializer = ItemSerializer(
                                item,
                                data={"to_list": True, "last_open_at": today},
                                partial=True,
                            )

                        if serializer.is_valid():
                            logger.info(f"{item.item_id}の更新成功")
                            serializer.save()
                        else:
                            logger.error(f"{item.item_id}の更新失敗")

                        # メッセージの送信
                        data = {
                            "replyToken": reply_token,
                            "messages": {
                                "type": "text",
                                "text": f"{item.item_name}を追加しました",
                            },
                        }

                        response = requests.post(reply_url, headers=headers, json=data)
                        if response.ok:
                            logger.info("買い物リスト追加通知の送信成功")
                        else:
                            logger.error(f"買い物リスト追加通知の送信失敗: {response.text}")

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
                    if response.ok:
                        logger.info("追加しない通知の送信成功")
                    else:
                        logger.error(f"追加しない通知の送信失敗: {response.text}")

        logger.info("Webhook処理終了")

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
