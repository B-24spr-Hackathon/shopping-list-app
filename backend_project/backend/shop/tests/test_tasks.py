import requests
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from unittest.mock import patch, call
from django.conf import settings
from shop.tasks import remind_request, shopping_request, remind_batch, shopping_batch
from shop.models import User, List, Item
from celery import current_app


"""
RemindRequestTestCase
remind_requestのテストケース
"""
class RemindRequestTestCase(TestCase):
    # 初期値を設定
    def setUp(self):
        self.line_id = "abcdefghijklmnopqrstuvwxyz"
        self.items1 = [
            {
                "item_id": 1,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 2,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 3,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 4,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 5,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 6,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 7,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 8,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 9,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 10,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
            {
                "item_id": 11,
                "item_name": "シャンプー",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            },
        ]

        self.items2 = [
            {
                "item_id": 12,
                "item_name": "石鹸",
                "consume_cycle": 30,
                "last_open_at": "2024-04-10",
            }
        ]

        self.start_log = "開封通知送信処理の開始"
        self.ok_log = f"{self.line_id}への通知成功"
        self.ng_log = f"{self.line_id}への通知失敗: "
        self.end_log = "開封通知送信処理の終了"

        # Celery設定を変更し同期的にタスクを呼出せるようにする
        self.celery_always_eager = current_app.conf.task_always_eager
        current_app.conf.task_always_eager = True

    # テスト終了後Celery設定を元に戻す
    def tearDown(self):
        current_app.conf.task_always_eager = self.celery_always_eager

    # itemsが2つ以上のリストの場合
    @patch("shop.tasks.logger")
    @patch("shop.tasks.requests.post")
    def test_several_items(self, mock_post, mock_logger):
        print("\n[[ RemindRequestTestCase/test_several_items(5) ]]")

        mock_post.return_value.ok = True

        expected_json = {
            "to": self.line_id,
            "messages": [
                {
                    "type": "template",
                    "altText": "開封確認",
                    "template": {
                        "type": "carousel",
                        "columns": [
                            {
                                "text": f"{self.items1[0]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[0]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[0]["item_name"],
                                    },
                                ],
                            },
                            {
                                "text": f"{self.items1[1]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[1]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[1]["item_name"],
                                    },
                                ],
                            },
                            {
                                "text": f"{self.items1[2]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[2]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[2]["item_name"],
                                    },
                                ],
                            },
                            {
                                "text": f"{self.items1[3]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[3]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[3]["item_name"],
                                    },
                                ],
                            },
                            {
                                "text": f"{self.items1[4]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[4]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[4]["item_name"],
                                    },
                                ],
                            },
                            {
                                "text": f"{self.items1[5]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[5]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[5]["item_name"],
                                    },
                                ],
                            },
                            {
                                "text": f"{self.items1[6]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[6]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[6]["item_name"],
                                    },
                                ],
                            },
                            {
                                "text": f"{self.items1[7]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[7]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[7]["item_name"],
                                    },
                                ],
                            },
                            {
                                "text": f"{self.items1[8]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[8]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[8]["item_name"],
                                    },
                                ],
                            },
                            {
                                "text": f"{self.items1[9]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[9]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[9]["item_name"],
                                    },
                                ],
                            },
                        ],
                    },
                },
                {
                    "type": "template",
                    "altText": "開封確認",
                    "template": {
                        "type": "carousel",
                        "columns": [
                            {
                                "text": f"{self.items1[10]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                                "actions": [
                                    {
                                        "type": "postback",
                                        "label": "追加する",
                                        "data": self.items1[10]["item_id"],
                                    },
                                    {
                                        "type": "postback",
                                        "label": "追加しない",
                                        "data": self.items1[10]["item_name"],
                                    },
                                ],
                            },
                        ],
                    },
                },
            ],
        }

        remind_request(self.line_id, self.items1)

        # LINE通知リクエストに渡されたargsを取得
        _, kwargs = mock_post.call_args

        # ログの呼出し内容と順番を定義
        expected_log = [
            call.info(self.start_log),
            call.info(self.ok_log),
            call.info(self.end_log),
        ]

        # ログが指定した順で呼出されたか確認
        mock_logger.info.assert_has_calls(expected_log)

        # ログ出力の確認
        print("[Result]: ", self.start_log)
        print("[Result]: ", self.ok_log)
        print("[Result]: ", self.end_log)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)

    # itemsが1つのリストの場合
    @patch("shop.tasks.logger")
    @patch("shop.tasks.requests.post")
    def test_one_items(self, mock_post, mock_logger):
        print("\n[[ RemindRequestTestCase/test_one_items(5) ]]")

        mock_post.return_value.ok = True

        expected_json = {
            "to": self.line_id,
            "messages": [
                {
                    "type": "template",
                    "altText": "開封確認",
                    "template": {
                        "type": "buttons",
                        "text": f"{self.items2[0]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                        "actions": [
                            {
                                "type": "postback",
                                "label": "追加する",
                                "data": self.items2[0]["item_id"],
                            },
                            {
                                "type": "postback",
                                "label": "追加しない",
                                "data": self.items2[0]["item_name"],
                            },
                        ]
                    }
                }
            ]
        }

        remind_request(self.line_id, self.items2)

        # LINE通知リクエストに渡されたargsを取得
        _, kwargs = mock_post.call_args

        # ログの呼出し内容と順番を定義
        expected_log = [
            call.info(self.start_log),
            call.info(self.ok_log),
            call.info(self.end_log),
        ]

        # ログが指定した順で呼出されたか確認
        mock_logger.info.assert_has_calls(expected_log)

        # ログ出力の確認
        print("[Result]: ", self.start_log)
        print("[Result]: ", self.ok_log)
        print("[Result]: ", self.end_log)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)

    # エラーレスポンスの場合
    @patch("shop.tasks.logger")
    @patch("shop.tasks.requests.post")
    def test_ng(self, mock_post, mock_logger):
        print("\n[[ RemindRequestTestCase/test_ng(5) ]]")

        # requests.postで例外を発生させる
        mock_post.return_value.status_code = 400
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()

        expected_json = {
            "to": self.line_id,
            "messages": [
                {
                    "type": "template",
                    "altText": "開封確認",
                    "template": {
                        "type": "buttons",
                        "text": f"{self.items2[0]['item_name']}がそろそろ無くなる頃です。\n買い物リストに追加しますか？",
                        "actions": [
                            {
                                "type": "postback",
                                "label": "追加する",
                                "data": self.items2[0]["item_id"],
                            },
                            {
                                "type": "postback",
                                "label": "追加しない",
                                "data": self.items2[0]["item_name"],
                            },
                        ],
                    },
                }
            ],
        }

        remind_request(self.line_id, self.items2)

        # LINE通知リクエストに渡されたargsを取得
        _, kwargs = mock_post.call_args

        # ログの呼出し内容と順番を定義
        expected_info_log = [
            call.info(self.start_log),
            call.info(self.end_log),
        ]

        # infoログが指定した順で呼出されたか確認
        mock_logger.info.assert_has_calls(expected_info_log)
        mock_logger.error.assert_called_once_with(self.ng_log + "HTTPError()")

        # ログ出力の確認
        print("[Result]: ", self.start_log)
        print("[Result]: ", self.ng_log)
        print("[Result]: ", self.end_log)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)


"""
ShoppingRequestTestCase
shopping_requestのテストケース
"""
class ShoppingRequestTestCase(TestCase):
    # 初期値を設定
    def setUp(self):
        self.line_id = "abcdefghijklmnopqrstuvwxyz"

        self.start_log = "買い物日通知送信処理の開始"
        self.ok_log = f"{self.line_id}への通知成功"
        self.ng_log = f"{self.line_id}への通知失敗: "
        self.end_log = "買い物日通知送信処理の終了"

        # Celery設定を変更し同期的にタスクを呼出せるようにする
        self.celery_always_eager = current_app.conf.task_always_eager
        current_app.conf.task_always_eager = True

    # テスト終了後Celery設定を元に戻す
    def tearDown(self):
        current_app.conf.task_always_eager = self.celery_always_eager

    # OKレスポンスの場合
    @patch("shop.tasks.logger")
    @patch("shop.tasks.requests.post")
    def test_ok(self, mock_post, mock_logger):
        print("\n[[ ShoppingRequestTestCase/test_ok(5) ]]")

        mock_post.return_value.ok = True

        expected_json = {
            "to": self.line_id,
            "messages": [
                {
                    "type": "template",
                    "altText": "買い物日通知",
                    "template": {
                        "type": "buttons",
                        "text": "明日は買い物予定日です！",
                        "actions": [
                            {
                                "type": "uri",
                                "label": "買い物リストを表示する",
                                "uri": settings.SHOPPING_LIST_URL,
                            }
                        ],
                    },
                }
            ],
        }

        shopping_request(self.line_id)

        # LINE通知リクエストに渡されたargsを取得
        _, kwargs = mock_post.call_args

        # ログの呼出し内容と順番を定義
        expected_log = [
            call.info(self.start_log),
            call.info(self.ok_log),
            call.info(self.end_log),
        ]

        # ログが指定した順で呼出されたか確認
        mock_logger.info.assert_has_calls(expected_log)

        # ログ出力の確認
        print("[Result]: ", self.start_log)
        print("[Result]: ", self.ok_log)
        print("[Result]: ", self.end_log)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)

    # エラーレスポンスの場合
    @patch("shop.tasks.logger")
    @patch("shop.tasks.requests.post")
    def test_ng(self, mock_post, mock_logger):
        print("\n[[ ShoppingRequestTestCase/test_ng(5) ]]")

        # requests.postで例外を発生させる
        mock_post.return_value.status_code = 400
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError()

        expected_json = {
            "to": self.line_id,
            "messages": [
                {
                    "type": "template",
                    "altText": "買い物日通知",
                    "template": {
                        "type": "buttons",
                        "text": "明日は買い物予定日です！",
                        "actions": [
                            {
                                "type": "uri",
                                "label": "買い物リストを表示する",
                                "uri": settings.SHOPPING_LIST_URL,
                            }
                        ],
                    },
                }
            ],
        }

        shopping_request(self.line_id)

        # LINE通知リクエストに渡されたargsを取得
        _, kwargs = mock_post.call_args

        # ログの呼出し内容と順番を定義
        expected_log = [
            call.info(self.start_log),
            call.info(self.end_log),
        ]

        # infoログが指定した順で呼出されたか確認
        mock_logger.info.assert_has_calls(expected_log)
        mock_logger.error.assert_called_once_with(self.ng_log + "HTTPError()")

        # ログ出力の確認
        print("[Result]: ", self.start_log)
        print("[Result]: ", self.ng_log)
        print("[Result]: ", self.end_log)
        # LINE通知リクエストが呼出された回数
        print("[Result]: ", mock_post.call_count, "==", 1)
        self.assertEqual(mock_post.call_count, 1)
        # LINE通知リクエストに渡されたkwargs（json）を確認
        print("[Result]: ", kwargs["json"])
        print("[Expect]: ", expected_json)
        self.assertEqual(kwargs["json"], expected_json)


"""
RemindBatchTestCase
remind_batchのテストケース
"""
class RemindBatchTestCase(TestCase):
    def setUp(self):
        # 初期値を設定
        self.user1 = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test"),
            line_id="abcdefghijklmnopqrstuvwxyz",
            line_status=True,
            have_list=True,
            remind=True,
            remind_timing=3,
            remind_time=datetime.strptime("18:00", "%H:%M").time()
        )

        list1 = List.objects.create(owner_id=self.user1)

        items1_data = [
            {
                "item_id": 1,
                "item_name": "洗剤",
                "list_id": list1,
                "consume_cycle": 30,
                "last_open_at": datetime.strptime("2024-03-01", "%Y-%m-%d").date(),
                "to_list": False,
                "remind_by_item": True,
                "manage_target": True,
            },
            {
                "item_id": 2,
                "item_name": "シャンプー",
                "list_id": list1,
                "consume_cycle": 30,
                "last_open_at": datetime.strptime("2024-04-01", "%Y-%m-%d").date(),
                "to_list": False,
                "remind_by_item": True,
                "manage_target": True,
            },
            {
                "item_id": 3,
                "item_name": "石鹸",
                "list_id": list1,
                "consume_cycle": 30,
                "last_open_at": datetime.strptime("2024-05-01", "%Y-%m-%d").date(),
                "to_list": False,
                "remind_by_item": True,
                "manage_target": True,
            },
        ]

        self.items1 = Item.objects.bulk_create([Item(**data) for data in items1_data])

        self.user2 = User.objects.create(
            user_id="hoge",
            user_name="hoge",
            email="hoge@sample.com",
            password=make_password("hoge"),
            line_id="12345abc67890",
            line_status=True,
            have_list=True,
            remind=True,
            remind_timing=0,
            remind_time=datetime.strptime("19:00", "%H:%M").time(),
        )

        list2 = List.objects.create(owner_id=self.user2)

        items2_data = [
            {
                "item_id": 4,
                "item_name": "洗剤",
                "list_id": list2,
                "consume_cycle": 30,
                "last_open_at": datetime.strptime("2024-03-01", "%Y-%m-%d").date(),
                "to_list": False,
                "remind_by_item": False,
                "manage_target": True,
            },
            {
                "item_id": 5,
                "item_name": "シャンプー",
                "list_id": list2,
                "consume_cycle": 30,
                "last_open_at": datetime.strptime("2024-04-01", "%Y-%m-%d").date(),
                "to_list": False,
                "remind_by_item": True,
                "manage_target": False,
            },
            {
                "item_id": 6,
                "item_name": "石鹸",
                "list_id": list2,
                "consume_cycle": 30,
                "last_open_at": datetime.strptime("2024-04-01", "%Y-%m-%d").date(),
                "to_list": False,
                "remind_by_item": True,
                "manage_target": True,
            },
        ]

        self.items2 = Item.objects.bulk_create([Item(**data) for data in items2_data])

    # user1: 2アイテム、user2: 1アイテムの通知
    @patch("shop.tasks.logger")
    @patch("shop.tasks.remind_request.apply_async")
    def test_ok(self, mock_remind_request, mock_logger):
        print("\n[[ RemindBatchTestCase/test_ok(8) ]]")

        # remind_requestに渡される予想される引数を定義
        expected_args1 = [
            self.user1.line_id,
            [
                {
                    "item_id": self.items1[0].item_id,
                    "item_name": self.items1[0].item_name
                },
                {
                    "item_id": self.items1[1].item_id,
                    "item_name": self.items1[1].item_name
                },
            ]
        ]

        expected_args2 = [
            self.user2.line_id,
            [
                {
                    "item_id": self.items2[2].item_id,
                    "item_name": self.items2[2].item_name
                }
            ],
        ]

        # タスクの実行
        remind_batch()

        # remind_requestに渡された引数を取得
        result_args = []
        for i in mock_remind_request.call_args_list:
            args, _ = i
            result_args.append(args)

        # ログの呼出し内容と順番を定義
        expected_log = [
            call.info("開封確認バッチ処理の開始"),
            call.info("開封通知ユーザー数: 2"),
            call.info("開封確認バッチ処理の終了"),
        ]

        # ログが指定した順で呼出されたか確認
        mock_logger.info.assert_has_calls(expected_log)
        # ログ出力の確認
        print("[Result]: 開封確認バッチ処理の開始")
        print("[Result]: 開封通知ユーザー数: 2")
        print("[Result]: 開封確認バッチ処理の終了")
        # remind_requestが呼出された回数
        print("[Result]: ", mock_remind_request.call_count, "==", 2)
        self.assertEqual(mock_remind_request.call_count, 2)
        # remind_requestに渡されたargsを確認
        print("[Result]: user1 line_id: ", result_args[1][0][0])
        print("[Expect]: user1 line_id: ", expected_args1[0])
        self.assertEqual(result_args[1][0][0], expected_args1[0])
        print("[Result]: user1 items: ", result_args[1][0][1])
        print("[Expect]: user1 items: ", expected_args1[1])
        self.assertEqual(result_args[1][0][1], expected_args1[1])
        print("[Result]: user2 line_id: ", result_args[0][0][0])
        print("[Expect]: user2 line_id: ", expected_args2[0])
        self.assertEqual(result_args[0][0][0], expected_args2[0])
        print("[Result]: user2 items: ", result_args[0][0][1])
        print("[Expect]: user2 items: ", expected_args2[1])
        self.assertEqual(result_args[0][0][1], expected_args2[1])


"""
ShoppingBatchTestCase
shopping_batchのテストケース
"""
class ShoppingBatchTestCase(TestCase):
    def setUp(self):
        # 初期値を設定
        self.user1 = User.objects.create(
            user_id="test",
            user_name="test",
            email="test@sample.com",
            password=make_password("test"),
            line_id="abcdefghijklmnopqrstuvwxyz",
            line_status=True,
            have_list=True,
            remind=True,
            remind_timing=3,
            remind_time=datetime.strptime("18:00", "%H:%M").time(),
        )

        list1_data = [
            {
                "list_id": 1,
                "list_name": "user1リスト1",
                "owner_id": self.user1,
                "shopping_day": 25,
            },
            {
                "list_id": 2,
                "list_name": "user1リスト2",
                "owner_id": self.user1,
                "shopping_day": 25,
            },
        ]

        List.objects.bulk_create([List(**data) for data in list1_data])

        self.user2 = User.objects.create(
            user_id="hoge",
            user_name="hoge",
            email="hoge@sample.com",
            password=make_password("hoge"),
            line_id="12345abc67890",
            line_status=True,
            have_list=True,
            remind=True,
            remind_timing=0,
            remind_time=datetime.strptime("19:00", "%H:%M").time(),
        )

        List.objects.create(list_id=3, list_name="user2リスト", owner_id=self.user2, shopping_day=25)

    # user1: 2アイテム、user2: 1アイテムの通知
    @patch("shop.tasks.logger")
    @patch("shop.tasks.shopping_request.apply_async")
    def test_ok(self, mock_shopping_request, mock_logger):
        print("\n[[ ShoppingBatchTestCase/test_ok(6) ]]")

        # shopping_requestに渡される予想される引数を定義
        expected_args1 = self.user1.line_id

        expected_args2 = self.user2.line_id

        # タスクの実行
        shopping_batch()

        # shopping_requestに渡された引数を取得
        result_args = []
        for i in mock_shopping_request.call_args_list:
            args, _ = i
            result_args.append(args)

        # ログの呼出し内容と順番を定義
        expected_log = [
            call.info("買い物日通知バッチ処理の開始"),
            call.info("買い物日通知ユーザー数: 2"),
            call.info("買い物日通知バッチ処理の終了"),
        ]

        # ログが指定した順で呼出されたか確認
        mock_logger.info.assert_has_calls(expected_log)
        # ログ出力の確認
        print("[Result]: 買い物日通知バッチ処理の開始")
        print("[Result]: 買い物日通知ユーザー数: 2")
        print("[Result]: 買い物日通知バッチ処理の終了")
        # shopping_requestが呼出された回数
        print("[Result]: ", mock_shopping_request.call_count, "==", 2)
        self.assertEqual(mock_shopping_request.call_count, 2)
        # shopping_requestに渡されたargsを確認
        print("[Result]: user1 line_id: ", result_args[0][0][0])
        print("[Expect]: user1 line_id: ", expected_args1)
        self.assertEqual(result_args[0][0][0], expected_args1)
        print("[Result]: user2 line_id: ", result_args[1][0][0])
        print("[Expect]: user2 line_id: ", expected_args2)
        self.assertEqual(result_args[1][0][0], expected_args2)
