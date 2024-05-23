import jwt
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch, call
from shop.tasks import remind_request, remind_batch
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


"""
RemindBatchTestCase
remind_batchのテストケース
"""
# class RemindBatchTestCase(TestCase):
#     def setUp(self):
#         # テスト用データのセットアップ
#         user = User.objects.create(
#             user_id="test",
#             line_id="U00db4ac5f595404949226fd28282f6d0",
#             remind_timing=0,
#             remind_time=(timezone.now() + timedelta(minutes=5)).time(),
#             line_status=True,
#             have_list=True,
#             remind=True,
#         )
#         list = List.objects.create(owner_id=user)
#         Item.objects.create(
#             list_id=list,
#             item_name="石鹸",
#             consume_cycle=5,
#             last_open_at=timezone.now().date() - timedelta(days=6),
#             remind_by_item=True,
#             manage_target=True,
#             to_list=False,
#         )

#     @patch("shop.message.remind_request.apply_async")
#     def test_remind_batch(self, mock_remind_request):
#         # タスクの実行
#         remind_batch()

#         # remind_requestが期待通りに呼出されたかを確認
#         self.assertTrue(mock_remind_request.called)
#         args, kwargs = mock_remind_request.call_args
#         print(args)
#         print(kwargs)
