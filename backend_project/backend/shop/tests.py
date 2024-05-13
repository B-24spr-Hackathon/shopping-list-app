from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch
from backend_project.backend.shop.tasks import remind_batch
from shop.models import User, List, Item
from datetime import timedelta


"""
RemindBatchTestCase
remind_batchのテストケース
"""
class RemindBatchTestCase(TestCase):
    def setUp(self):
        # テスト用データのセットアップ
        user = User.objects.create(
            user_id="test",
            line_id="U00db4ac5f595404949226fd28282f6d0",
            remind_timing=0,
            remind_time=(timezone.now() + timedelta(minutes=5)).time(),
            line_status=True,
            have_list=True,
            remind=True,
        )
        list = List.objects.create(owner_id=user)
        Item.objects.create(
            list_id=list,
            item_name="石鹸",
            consume_cycle=5,
            last_open_at=timezone.now().date() - timedelta(days=6),
            remind_by_item=True,
            manage_target=True,
            to_list=False)

    @patch("shop.message.remind_request.apply_async")
    def test_remind_batch(self, mock_remind_request):
        # タスクの実行
        remind_batch()

        # remind_requestが期待通りに呼出されたかを確認
        self.assertTrue(mock_remind_request.called)
        args, kwargs = mock_remind_request.call_args
        print(args)
        print(kwargs)
