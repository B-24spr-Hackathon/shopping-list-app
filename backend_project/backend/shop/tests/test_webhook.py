import jwt, time, base64, hashlib, hmac, json
from datetime import timedelta, datetime
from unittest.mock import patch, MagicMock
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import User, List, Member, Item


# 全テスト同じ項目を定義
url = reverse("line-webhook")
redirect_url = settings.LINK_REDIRECT_URL
secret = settings.LINE_MESSAGE_SECRET

"""
LineWebhookViewTestCase
LineWebhookViewクラスPOSTリクエストのテストケース
"""
class LineWebhookViewTestCase(APITestCase):
    # 初期値を設定
    def setUp(self):
        # user1（line_id無し、line_status: False）
        self.user1 = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test"),
        )
        self.user1.save()

        # user1用のLINE連携用JWTを生成
        payload = {
            "user_id": self.user1.user_id,
            "exp": timezone.now() + timedelta(minutes=10),
            "iat": timezone.now()
        }
        self.token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        # user2（line_id有り、line_status: True）
        self.user2 = User.objects.create(
            user_id="hoge",
            user_name="hoge",
            email="hoge@sample.com",
            password=make_password("hoge"),
            line_id="abcdefghijklmnopqrstuvwxyz",
            line_status=True
        )
        self.user2.save()

        # user3（line_id有り、line_status: False）
        self.user3 = User.objects.create(
            user_id="fuga",
            user_name="fuga",
            email="fuga@sample.com",
            password=make_password("fuga"),
            line_id="123456789abc123456789",
            line_status=False,
        )
        self.user3.save()

        # user2のlist
        self.list = List.objects.create(
            owner_id=self.user2,
            list_name="hoge-list",
            shopping_day=5
        )
        self.list.save()

        # user2のitem
        self.item = Item.objects.create(
            item_name="洗剤",
            list_id=self.list,
            consume_cycle=120,
            last_purchase_at="2024-02-20",
            last_open_at="2024-03-01",
            to_list=False
        )

    # 署名を作成するメソッド
    def make_signature(self, data):
        encode = json.dumps(data, ensure_ascii=False).replace(" ", "").encode("utf-8")
        hash = hmac.new(secret.encode("utf-8"), encode, hashlib.sha256).digest()
        signature = base64.b64encode(hash).decode("utf-8")
        return signature

    # 疎通確認のリクエスト（空のボディ）
    @patch("shop.views.webhook.logger")
    def test_empty_request(self, mock_logger):
        print("\n[[ LineWebhookViewTestCase/test_empty_request(2) ]]")

        # リクエストデータを定義
        data = {}

        # 期待されるログ出力を定義
        expected_log = "webhook疎通確認"

        response = self.client.post(url, data=data, format="json")

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ログ出力の確認
        print("[Result]: ", expected_log)
        mock_logger.info.assert_called_with(expected_log)

    # 疎通確認のリクエスト（空のevents）
    @patch("shop.views.webhook.logger")
    def test_empty_events(self, mock_logger):
        print("\n[[ LineWebhookViewTestCase/test_empty_events(2) ]]")

        # リクエストデータを定義
        data = {"destination": "xxxxxxxxxx", "events": []}

        # 期待されるログ出力を定義
        expected_log = "webhook疎通確認"

        response = self.client.post(url, data=data, format="json")

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ログ出力の確認
        print("[Result]: ", expected_log)
        mock_logger.info.assert_called_with(expected_log)

    # LINE連携のリクエスト（LINEメッセージ送信リクエストはモック）
    @patch("shop.views.webhook.requests.post")
    def test_line_link(self, mock_post):
        print("\n[[ LineWebhookViewTestCase/test_line_link(4) ]]")
        # モック化したLINEメッセージ送信リクエストのレスポンスを定義
        mock_post.return_value = MagicMock(ok=True)

        # リクエストデータを定義
        data = {
            "destination":"xxxxxxxxxx",
            "events":[
                {
                    "type": "message",
                    "message": {
                        "type": "text",
                        "id": "123456789",
                        "text": str(self.token)
                    },
                    "timestamp": int(time.time() * 1000),
                    "source": {
                        "type": "user",
                        "userId": "abc123def456ghi789"
                    },
                    "replyToken": "757913772c4646b784d4b7ce46d12671",
                    "mode": "active",
                    "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                    "deliveryContext": {"isRedelivery": False}
                }
            ]
        }

        # リクエスト送信後のuser1のデータを定義
        expected_db = {
            "user_id": "test",
            "user_name": "test",
            "email": "test@sample.com",
            "line_id": "abc123def456ghi789",
            "line_status": True,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # LINE通知リクエストに渡されるべきデータを定義
        expected_json = {
            "replyToken": data["events"][0]["replyToken"],
            "messages": {
                "type": "text",
                "text": f"{self.user1.user_name}さん\n友達追加ありがとうございます！\nアプリへ戻って設定の続きをお願いします\n\n{redirect_url}",
            },
        }

        # ヘッダーに付与する署名を生成
        signature = self.make_signature(data)

        # リクエストのヘッダーを定義
        headers = {"x-line-signature": signature}

        response = self.client.post(url, data=data, headers=headers, format="json")

        # DBからuser1のデータを取得
        user = User.objects.filter(user_id=self.user1.user_id).values(
            "user_id",
            "user_name",
            "email",
            "line_id",
            "line_status",
            "user_icon",
            "invitation",
            "request",
            "have_list",
            "default_list",
            "remind",
            "remind_timing",
            "remind_time",
        )

        # LINE通知リクエストに渡されたkwargs（json）を取得
        _, kwargs = mock_post.call_args

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", expected_db)
        self.assertEqual(user[0], expected_db)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)

    # 友達追加のリクエスト（LINEメッセージ送信リクエストはモック）
    @patch("shop.views.webhook.requests.post")
    def test_follow_event(self, mock_post):
        print("\n[[ LineWebhookViewTestCase/test_follow_event(4) ]]")
        # モック化したLINEメッセージ送信リクエストのレスポンスを定義
        mock_post.return_value = MagicMock(ok=True)

        # リクエストデータを定義
        data = {
            "destination": "xxxxxxxxxx",
            "events": [
                {
                    "type": "follow",
                    "timestamp": int(time.time() * 1000),
                    "source": {
                        "type": "user",
                        "userId": "123456789abc123456789"
                    },
                    "replyToken": "757913772c4646b784d4b7ce46d12671",
                    "mode": "active",
                    "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                    "deliveryContext": {"isRedelivery": False},
                }
            ],
        }

        # リクエスト送信後のuser1のデータを定義
        expected_db = {
            "user_id": "fuga",
            "user_name": "fuga",
            "email": "fuga@sample.com",
            "line_id": "123456789abc123456789",
            "line_status": True,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # LINE通知リクエストに渡されるべきデータを定義
        expected_json = {
            "replyToken": data["events"][0]["replyToken"],
            "messages": {
                "type": "text",
                "text": "友だち追加ありがとうございます！\n買いもっとからの通知をお待ちください m _ _ m",
            },
        }

        # ヘッダーに付与する署名を生成
        signature = self.make_signature(data)

        # リクエストのヘッダーを定義
        headers = {"x-line-signature": signature}

        response = self.client.post(url, data=data, headers=headers, format="json")

        # DBからuser3のデータを取得
        user = User.objects.filter(user_id=self.user3.user_id).values(
            "user_id",
            "user_name",
            "email",
            "line_id",
            "line_status",
            "user_icon",
            "invitation",
            "request",
            "have_list",
            "default_list",
            "remind",
            "remind_timing",
            "remind_time",
        )

        # LINE通知リクエストに渡されたkwargs（json）を取得
        _, kwargs = mock_post.call_args

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", expected_db)
        self.assertEqual(user[0], expected_db)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)

    # 友達追加解除のリクエスト
    def test_unfollow_event(self):
        print("\n[[ LineWebhookViewTestCase/test_unfollow_event(2) ]]")

        # リクエストデータを定義
        data = {
            "destination": "xxxxxxxxxx",
            "events": [
                {
                    "type": "unfollow",
                    "timestamp": int(time.time() * 1000),
                    "source": {
                        "type": "user",
                        "userId": "abcdefghijklmnopqrstuvwxyz"
                    },
                    "mode": "active",
                    "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                    "deliveryContext": {"isRedelivery": False},
                }
            ],
        }

        # リクエスト送信後のuser1のデータを定義
        expected_db = {
            "user_id": "hoge",
            "user_name": "hoge",
            "email": "hoge@sample.com",
            "line_id": "abcdefghijklmnopqrstuvwxyz",
            "line_status": False,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # ヘッダーに付与する署名を生成
        signature = self.make_signature(data)

        # リクエストのヘッダーを定義
        headers = {"x-line-signature": signature}

        response = self.client.post(url, data=data, headers=headers, format="json")

        # DBからuser2のデータを取得
        user = User.objects.filter(user_id=self.user2.user_id).values(
            "user_id",
            "user_name",
            "email",
            "line_id",
            "line_status",
            "user_icon",
            "invitation",
            "request",
            "have_list",
            "default_list",
            "remind",
            "remind_timing",
            "remind_time",
        )

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", expected_db)
        self.assertEqual(user[0], expected_db)

    # アイテム追加のリクエスト（LINEメッセージ送信リクエストはモック）
    @patch("shop.views.webhook.requests.post")
    def test_postback_yes_event(self, mock_post):
        print("\n[[ LineWebhookViewTestCase/test_postback_yes_event(4) ]]")
        # モック化したLINEメッセージ送信リクエストのレスポンスを定義
        mock_post.return_value = MagicMock(ok=True)

        # リクエストデータを定義
        data = {
            "destination":"xxxxxxxxxx",
            "events":[
                {
                    "type":"postback",
                    "timestamp":int(time.time() * 1000),
                    "source":{
                        "type":"user",
                        "userId":"123456789abc123456789"
                    },
                    "replyToken":"757913772c4646b784d4b7ce46d12671",
                    "mode":"active",
                    "webhookEventId":"01FZ74A0TDDPYRVKNK77XKC3ZR",
                    "deliveryContext":{
                        "isRedelivery":False
                    },
                    "postback": {
                        "data": self.item.item_id,
                        "params": {}
                    }
                }
            ]
        }

        today = timezone.now().date()
        last_open_at = datetime.strptime(self.item.last_open_at, "%Y-%m-%d").date()
        new_cycle = (today - last_open_at).days

        # リクエスト送信後のuser1のデータを定義
        expected_db = {
            "item_name": self.item.item_name,
            "list_id": self.item.list_id.list_id,
            "consume_cycle": new_cycle,
            "last_purchase_at": datetime.strptime("2024-02-20", "%Y-%m-%d").date(),
            "last_open_at": today,
            "to_list": True,
        }

        # LINE通知リクエストに渡されるべきデータを定義
        expected_json = {
            "replyToken": data["events"][0]["replyToken"],
            "messages": {
                "type": "text",
                "text": f"{self.item.item_name}を追加しました",
            },
        }

        # ヘッダーに付与する署名を生成
        signature = self.make_signature(data)

        # リクエストのヘッダーを定義
        headers = {"x-line-signature": signature}

        response = self.client.post(url, data=data, headers=headers, format="json")

        # DBからitemのデータを取得
        item = Item.objects.filter(item_id=self.item.item_id).values(
            "item_name",
            "list_id",
            "consume_cycle",
            "last_purchase_at",
            "last_open_at",
            "to_list"
        )

        # LINE通知リクエストに渡されたkwargs（json）を取得
        _, kwargs = mock_post.call_args

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DBデータの確認
        print("[Result]: ", item[0])
        print("[Expect]: ", expected_db)
        self.assertEqual(item[0], expected_db)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)

    # アイテム追加済みのリクエスト（LINEメッセージ送信リクエストはモック）
    @patch("shop.views.webhook.requests.post")
    def test_postback_already_event(self, mock_post):
        print("\n[[ LineWebhookViewTestCase/test_postback_already_event(4) ]]")
        # モック化したLINEメッセージ送信リクエストのレスポンスを定義
        mock_post.return_value = MagicMock(ok=True)

        # itemのto_listをTrueに変更
        self.item.to_list = True
        self.item.save()

        # リクエストデータを定義
        data = {
            "destination": "xxxxxxxxxx",
            "events": [
                {
                    "type": "postback",
                    "timestamp": int(time.time() * 1000),
                    "source": {
                        "type": "user",
                        "userId": "123456789abc123456789"
                    },
                    "replyToken": "757913772c4646b784d4b7ce46d12671",
                    "mode": "active",
                    "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                    "deliveryContext": {"isRedelivery": False},
                    "postback": {
                        "data": self.item.item_id,
                        "params": {}
                    },
                }
            ],
        }

        # リクエスト送信後のuser1のデータを定義
        expected_db = {
            "item_name": self.item.item_name,
            "list_id": self.item.list_id.list_id,
            "consume_cycle": 120,
            "last_purchase_at": datetime.strptime("2024-02-20", "%Y-%m-%d").date(),
            "last_open_at": datetime.strptime("2024-03-01", "%Y-%m-%d").date(),
            "to_list": True,
        }

        # LINE通知リクエストに渡されるべきデータを定義
        expected_json = {
            "replyToken": data["events"][0]["replyToken"],
            "messages": {
                "type": "text",
                "text": f"{self.item.item_name}は既に追加済みです",
            },
        }

        # ヘッダーに付与する署名を生成
        signature = self.make_signature(data)

        # リクエストのヘッダーを定義
        headers = {"x-line-signature": signature}

        response = self.client.post(url, data=data, headers=headers, format="json")

        # DBからitemのデータを取得
        item = Item.objects.filter(item_id=self.item.item_id).values(
            "item_name",
            "list_id",
            "consume_cycle",
            "last_purchase_at",
            "last_open_at",
            "to_list",
        )

        # LINE通知リクエストに渡されたkwargs（json）を取得
        _, kwargs = mock_post.call_args

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DBデータの確認
        print("[Result]: ", item[0])
        print("[Expect]: ", expected_db)
        self.assertEqual(item[0], expected_db)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)

    # アイテム追加しないリクエスト（LINEメッセージ送信リクエストはモック）
    @patch("shop.views.webhook.requests.post")
    def test_postback_no_event(self, mock_post):
        print("\n[[ LineWebhookViewTestCase/test_postback_no_event(4) ]]")
        # モック化したLINEメッセージ送信リクエストのレスポンスを定義
        mock_post.return_value = MagicMock(ok=True)

        # リクエストデータを定義
        data = {
            "destination": "xxxxxxxxxx",
            "events": [
                {
                    "type": "postback",
                    "timestamp": int(time.time() * 1000),
                    "source": {
                        "type": "user",
                        "userId": "123456789abc123456789"
                    },
                    "replyToken": "757913772c4646b784d4b7ce46d12671",
                    "mode": "active",
                    "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                    "deliveryContext": {"isRedelivery": False},
                    "postback": {
                        "data": self.item.item_name,
                        "params": {}
                    },
                }
            ],
        }

        # リクエスト送信後のuser1のデータを定義
        expected_db = {
            "item_name": self.item.item_name,
            "list_id": self.item.list_id.list_id,
            "consume_cycle": 120,
            "last_purchase_at": datetime.strptime("2024-02-20", "%Y-%m-%d").date(),
            "last_open_at": datetime.strptime("2024-03-01", "%Y-%m-%d").date(),
            "to_list": False,
        }

        # LINE通知リクエストに渡されるべきデータを定義
        expected_json = {
            "replyToken": data["events"][0]["replyToken"],
            "messages": {
                "type": "text",
                "text": f"{self.item.item_name}を追加しませんでした",
            },
        }

        # ヘッダーに付与する署名を生成
        signature = self.make_signature(data)

        # リクエストのヘッダーを定義
        headers = {"x-line-signature": signature}

        response = self.client.post(url, data=data, headers=headers, format="json")

        # DBからitemのデータを取得
        item = Item.objects.filter(item_id=self.item.item_id).values(
            "item_name",
            "list_id",
            "consume_cycle",
            "last_purchase_at",
            "last_open_at",
            "to_list",
        )

        # LINE通知リクエストに渡されたkwargs（json）を取得
        _, kwargs = mock_post.call_args

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DBデータの確認
        print("[Result]: ", item[0])
        print("[Expect]: ", expected_db)
        self.assertEqual(item[0], expected_db)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)

    # JWT以外のテキストメッセージリクエスト（LINEメッセージ送信リクエストはモック）
    @patch("shop.views.webhook.requests.post")
    def test_not_jwt(self, mock_post):
        print("\n[[ LineWebhookViewTestCase/test_not_jwt(4) ]]")
        # モック化したLINEメッセージ送信リクエストのレスポンスを定義
        mock_post.return_value = MagicMock(ok=True)

        # リクエストデータを定義
        data = {
            "destination": "xxxxxxxxxx",
            "events": [
                {
                    "type": "message",
                    "message": {
                        "type": "text",
                        "id": "123456789",
                        "text": "こんにちわ！",
                    },
                    "timestamp": int(time.time() * 1000),
                    "source": {
                        "type": "user",
                        "userId": "abcdefghijklmnopqrstuvwxyz"
                    },
                    "replyToken": "757913772c4646b784d4b7ce46d12671",
                    "mode": "active",
                    "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                    "deliveryContext": {"isRedelivery": False},
                }
            ],
        }

        # リクエスト送信後のuser2のデータを定義
        expected_db = {
            "user_id": "hoge",
            "user_name": "hoge",
            "email": "hoge@sample.com",
            "line_id": "abcdefghijklmnopqrstuvwxyz",
            "line_status": True,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # LINE通知リクエストに渡されるべきデータを定義
        expected_json = {
            "replyToken": data["events"][0]["replyToken"],
            "messages": {
                "type": "text",
                "text": "メッセージありがとうございます！\n買いもっとでは通知のみを行っており、メッセージは受付けておりません m _ _ m",
            },
        }

        # ヘッダーに付与する署名を生成
        signature = self.make_signature(data)

        # リクエストのヘッダーを定義
        headers = {"x-line-signature": signature}

        response = self.client.post(url, data=data, headers=headers, format="json")

        # DBからuser2のデータを取得
        user = User.objects.filter(user_id=self.user2
                                   .user_id).values(
            "user_id",
            "user_name",
            "email",
            "line_id",
            "line_status",
            "user_icon",
            "invitation",
            "request",
            "have_list",
            "default_list",
            "remind",
            "remind_timing",
            "remind_time",
        )

        # LINE通知リクエストに渡されたkwargs（json）を取得
        _, kwargs = mock_post.call_args

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", expected_db)
        self.assertEqual(user[0], expected_db)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)

    # テキスト以外のメッセージリクエスト（LINEメッセージ送信リクエストはモック）
    @patch("shop.views.webhook.requests.post")
    def test_not_text(self, mock_post):
        print("\n[[ LineWebhookViewTestCase/test_not_text(4) ]]")
        # モック化したLINEメッセージ送信リクエストのレスポンスを定義
        mock_post.return_value = MagicMock(ok=True)

        # リクエストデータを定義
        data = {
            "destination": "xxxxxxxxxx",
            "events": [
                {
                    "type": "message",
                    "message": {
                        "type": "audio",
                        "id": "123456789",
                        "duration": 60000,
                        "contentProvider": {"type": "line"},
                    },
                    "timestamp": int(time.time() * 1000),
                    "source": {
                        "type": "user",
                        "userId": "abcdefghijklmnopqrstuvwxyz"
                    },
                    "replyToken": "757913772c4646b784d4b7ce46d12671",
                    "mode": "active",
                    "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
                    "deliveryContext": {"isRedelivery": False},
                }
            ],
        }

        # リクエスト送信後のuser2のデータを定義
        expected_db = {
            "user_id": "hoge",
            "user_name": "hoge",
            "email": "hoge@sample.com",
            "line_id": "abcdefghijklmnopqrstuvwxyz",
            "line_status": True,
            "user_icon": None,
            "invitation": False,
            "request": False,
            "have_list": False,
            "default_list": True,
            "remind": False,
            "remind_timing": 0,
            "remind_time": None,
        }

        # LINE通知リクエストに渡されるべきデータを定義
        expected_json = {
            "replyToken": data["events"][0]["replyToken"],
            "messages": {
                "type": "text",
                "text": "ありがとうございます！\n買いもっとでは通知のみを行っており、メッセージは受付けておりません m _ _ m",
            },
        }

        # ヘッダーに付与する署名を生成
        signature = self.make_signature(data)

        # リクエストのヘッダーを定義
        headers = {"x-line-signature": signature}

        response = self.client.post(url, data=data, headers=headers, format="json")

        # DBからuser2のデータを取得
        user = User.objects.filter(user_id=self.user2.user_id).values(
            "user_id",
            "user_name",
            "email",
            "line_id",
            "line_status",
            "user_icon",
            "invitation",
            "request",
            "have_list",
            "default_list",
            "remind",
            "remind_timing",
            "remind_time",
        )

        # LINE通知リクエストに渡されたkwargs（json）を取得
        _, kwargs = mock_post.call_args

        # HTTPステータスコードの確認
        print("[Result]: ", response.status_code, "==", status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DBデータの確認
        print("[Result]: ", user[0])
        print("[Expect]: ", expected_db)
        self.assertEqual(user[0], expected_db)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)
