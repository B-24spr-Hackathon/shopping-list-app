import jwt
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import User


"""
UserGetViewTestCase
UserViewクラスGETリクエストのテストケース
"""
# class UserGetViewTestCase(APITestCase):
#     # テスト用データのセットアップ
#     def setUp(self):
#         User.objects.create(
#             user_id="test", user_name="test", email="test@sample.com", password="test"
#         )

#     def test_ok_data(self):
#         print("[[ UserGetViewTestCase/test_ok_data(4) ]]")
#         url = reverse("user")
#         data = {"email": "test@sample.com", "password": "test"}

#         expected_response = {
#             "user_id": "test",
#             "user_name": "test",
#             "email": "test@sample.com",
#             "line_id": None,
#             "line_status": False,
#             "user_icon": None,
#             "invitation": False,
#             "request": False,
#             "have_list": False,
#             "dafault_list": True,
#             "remind": False,
#             "remind_timing": 0,
#             "remind_time": None,
#         }

#         response = self.client.post(url, data, format="json")

#         # レスポンスからJWTを抜出す
#         try:
#             response_jwt = response.data["access"]
#             user_id = self.verify_jwt(response_jwt)
#         except:
#             user_id = False
#             print("[Result]: ", "JWT付与なし")

#         # HTTPステータスコードの確認
#         print("[Result]: ", response.status_code, "==", status.HTTP_201_CREATED)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # 登録されたレコード数の確認
#         print("[Result]: ", User.objects.count(), "==", 1)
#         self.assertEqual(User.objects.count(), 1)
#         # レスポンスデータ（user部分）の確認
#         print("[Result]: ", response.data["user"], "==", expected_response)
#         self.assertEqual(response.data["user"], expected_response)
#         # JWTの確認
#         print("[Result]: ", user_id, "==", "test")
#         self.assertEqual(user_id, "test")
